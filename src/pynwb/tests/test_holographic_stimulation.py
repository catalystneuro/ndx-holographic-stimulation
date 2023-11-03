from datetime import datetime
import numpy as np
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing.mock.device import mock_Device
from pynwb.testing.mock.ophys import (
    mock_ImagingPlane,
    mock_OpticalChannel,
    mock_PlaneSegmentation,
)
from pynwb import NWBFile, NWBHDF5IO
from ndx_holographic_stimulation import (
    HolographicSeries,
    HolographicStimulusSite,
    HolographicStimulusPattern,
)
from pynwb.ophys import ImageSegmentation, OpticalChannel
from hdmf.testing import TestCase
from numpy.testing import assert_array_equal
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from warnings import warn


class TestHolographicSeries(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session_start_time = datetime.now().astimezone()
        cls.site_name = "HolographicStimulusSite"  # TODO REMOVE
        cls.test_dir = Path(mkdtemp())

    def setUp(self) -> None:
        self.nwbfile = mock_NWBFile(session_start_time=self.session_start_time)
        self.device = mock_Device(nwbfile=self.nwbfile)
        self.optical_channel = mock_OpticalChannel(nwbfile=self.nwbfile)
        self.imaging_plane = mock_ImagingPlane(
            optical_channel=self.optical_channel,
            device=self.device,
            nwbfile=self.nwbfile,
        )
        self.n_rois = 2
        self.plane_segmentation = mock_PlaneSegmentation(
            imaging_plane=self.imaging_plane, n_rois=self.n_rois, nwbfile=self.nwbfile
        )

        self.roi_table_region = self.plane_segmentation.create_roi_table_region(
            region=[0, 1], description="the first of two ROIs"
        )
        # metadata for holographic series #TODO add the others

    @classmethod
    def tearDownClass(cls):
        try:
            rmtree(cls.test_dir)
        except PermissionError:  # Windows CI bug
            warn(
                f"Unable to fully clean the temporary directory: {cls.test_dir}\n\nPlease remove it manually."
            )

    def test_holographic_series_constructor(self):
        stimulus_pattern = HolographicStimulusPattern(
            name="stimulus_pattern",
            description="spiral, 5 revolutions, 5 repetitions",  # TODO: fix the name definition
        )
        
        
        holo_stim_site = HolographicStimulusSite(
            name=self.site_name,
            device=self.device,
            description="This is an example holographic site.",
            excitation_lambda=600.0,  # nm
            effector="ChR2",
            location="VISrl",
            stimulus_pattern=stimulus_pattern,
        )
        self.nwbfile.add_ogen_site(holo_stim_site)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        holographic_stimulation = HolographicSeries(
            name="holographic_stimulation",
            description="Holographic stimulus on 2 rois",
            data=data,
            unit="W",
            rois=self.roi_table_region,
            site=holo_stim_site,
            timestamps=timestamps,
        )

        self.nwbfile.add_stimulus(holographic_stimulation)

        self.assertIn(holographic_stimulation, self.nwbfile.stimulus)
        assert_array_equal(self.nwbfile.stimulus["holographic_stimulation"].data, data)

    def test_holographic_series_roundtrip(self):
        stimulus_pattern = HolographicStimulusPattern(
            name="stimulus_pattern",
            description="spiral, 5 revolutions, 5 repetitions",  # TODO: fix the name definition
        )


        holo_stim_site = HolographicStimulusSite(
            name=self.site_name,
            device=self.device,
            description="This is an example holographic site.",
            excitation_lambda=600.0,  # nm
            effector="ChR2",
            location="VISrl",
            stimulus_pattern=stimulus_pattern,
        )
        self.nwbfile.add_ogen_site(holo_stim_site)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        holographic_stimulation = HolographicSeries(
            name="holographic_stimulation",
            description="Holographic stimulus on 2 rois",
            data=data,
            unit="W",
            rois=self.roi_table_region,
            site=holo_stim_site,
            timestamps=timestamps,
        )

        self.nwbfile.add_stimulus(holographic_stimulation)

        nwbfile_path = self.test_dir / "test_holographic_stimulation_nwb.nwb"
        with NWBHDF5IO(nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            nwbfile_in = io.read()
            # device_metadata = deepcopy(self.miniscope_mscam_metadata)
            # device_name = device_metadata.pop("name")
            # self.assertIn(device_name, nwbfile_in.devices)
            # device_in = nwbfile_in.devices[device_name]
            # self.assertDictEqual(device_in.fields, device_metadata)
