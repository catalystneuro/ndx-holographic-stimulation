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
    SpiralScanning,
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
        # metadata for holographic series
        self.series_name = "HolographicSeries"
        self.series_description = "Holographic stimulus on 2 rois"
        self.unit = "watts"
        # metadata for holographic stimulus site
        self.site_name = "HolographicStimulusSite"
        self.site_description = "This is an example holographic site."
        self.excitation_lambda = 600.0
        self.effector = "ChR2"
        self.location = "VISrl"
        # metadata for holographic stimulus pattern
        self.pattern_name = "HolographicStimulusPattern"
        self.pattern_description = "Spiral scanning beam pattern"
        self.spiral_duration=15e-3
        self.spiral_diameter=15e-6
        self.spiral_height=10e-6
        self.num_revolutions=5
        self.num_spirals=5
        self.isi_spiral=10e-3

    @classmethod
    def tearDownClass(cls):
        try:
            rmtree(cls.test_dir)
        except PermissionError:  # Windows CI bug
            warn(
                f"Unable to fully clean the temporary directory: {cls.test_dir}\n\nPlease remove it manually."
            )

    def test_holographic_series_constructor(self):
        spiral_scanning=SpiralScanning(
            spiral_duration=self.spiral_duration,
            spiral_diameter=self.spiral_diameter,
            spiral_height=self.spiral_height,
            num_revolutions=self.num_revolutions,
            num_spirals=self.num_spirals,
            isi_spiral=self.isi_spiral,
            description=self.pattern_description
        )
        stimulus_pattern = HolographicStimulusPattern(
            name=self.pattern_name,
            description=self.pattern_description,
            spiral_scanning=spiral_scanning,
        )
        self.nwbfile.add_lab_meta_data(stimulus_pattern)

        holo_stim_site = HolographicStimulusSite(
            name=self.site_name,
            device=self.device,
            description=self.site_description,
            excitation_lambda=self.excitation_lambda,  # nm
            effector=self.effector,
            location=self.location,
            stimulus_pattern=stimulus_pattern,
        )
        self.nwbfile.add_ogen_site(holo_stim_site)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        holographic_stimulation = HolographicSeries(
            name=self.series_name,
            description=self.series_description,
            data=data,
            unit=self.unit,
            rois=self.roi_table_region,
            site=holo_stim_site,
            timestamps=timestamps,
        )
        assert_array_equal(holographic_stimulation.data, data)

        self.nwbfile.add_stimulus(holographic_stimulation)

        assert holographic_stimulation.name in self.nwbfile.stimulus.keys()
        assert holographic_stimulation in self.nwbfile.stimulus.values()

    def test_holographic_series_roundtrip(self):
        stimulus_pattern = HolographicStimulusPattern()
        self.nwbfile.add_lab_meta_data(
            stimulus_pattern
        )  # TODO extend stimulus pattern a timeseries and add to stimulus module or a labmetadata and add to general

        holo_stim_site = HolographicStimulusSite(
            name=self.site_name,
            device=self.device,
            description=self.site_description,
            excitation_lambda=self.excitation_lambda,  # nm
            effector=self.effector,
            location=self.location,
            stimulus_pattern=stimulus_pattern,
        )
        self.nwbfile.add_ogen_site(holo_stim_site)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        holographic_stimulation = HolographicSeries(
            name=self.series_name,
            description=self.series_description,
            data=data,
            unit=self.unit,
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
            assert self.series_name in nwbfile_in.stimulus.keys()
            # device_metadata = deepcopy(self.miniscope_mscam_metadata)
            # device_name = device_metadata.pop("name")
            # self.assertIn(device_name, nwbfile_in.devices)
            # device_in = nwbfile_in.devices[device_name]
            # self.assertDictEqual(device_in.fields, device_metadata)
