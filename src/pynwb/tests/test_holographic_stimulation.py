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
    PatternedOptogeneticSeries,
    PatternedOptogeneticStimulusSite,
    OptogeneticStimulusPattern,
    SpiralScanning,
    TemporalFocusing,
    SpatialLightModulator,
    LightSource,
)
from pynwb.ophys import ImageSegmentation, OpticalChannel
from hdmf.testing import TestCase
from numpy.testing import assert_array_equal
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from warnings import warn


class TestPatternedOptogeneticSeries(TestCase):
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
        # metadata for Patterned series
        self.series_name = "PatternedOptogeneticSeries"
        self.series_description = "Patterned stimulus on 2 rois"
        self.unit = "watts"
        # metadata for Patterned stimulus site
        self.site_name = "StimulusSite"
        self.site_description = "This is an example Patterned site."
        self.effector = "ChR2"
        self.location = "VISrl"
        # metadata for  stimulus pattern
        self.pattern_name = "StimulusPattern"
        self.pattern_description = "beam pattern"
        self.duration = 10e-3
        self.number_of_stimulus_presentation = 10
        self.inter_stimulus_interval = 0.02
        # metadata for spiral scanning pattern
        self.spiral_scanning_name = "SpiralScanning"
        self.spiral_diameter = 15e-6
        self.spiral_height = 10e-6
        self.num_revolutions = 5
        # metadata for temporal focusing pattern
        self.temporal_focusing_name = "TemporalFocusing"
        self.lateral_psf = "9e-6 m ± 0.7e-6 m"
        self.axial_psf = "32e-6 m ± 1.6e-6 m"
        # metadata for spiatial light modulator
        self.slm_name = "SpatialLightModulator"
        self.slm_description = "Generic description for the slm"
        self.slm_model = "model"
        self.slm_resolution = 1.
        # metadata for the light source
        self.light_source_name = "Generic Laser"
        self.light_source_description = "Generic description for the laser"
        self.light_source_manifacturer = "manifacturer"
        self.stimulation_wavelenght = 600.0
        self.filter = "600/50"
        self.power = 8.
        self.intensity = 100. 
        self.exposure_time = 1e-6
        self.pulse_rate = 1/self.exposure_time 

    @classmethod
    def tearDownClass(cls):
        try:
            rmtree(cls.test_dir)
        except PermissionError:  # Windows CI bug
            warn(
                f"Unable to fully clean the temporary directory: {cls.test_dir}\n\nPlease remove it manually."
            )

    def test_patterned_optogenetic_series_constructor_with_spiralscanning(self):
        spiral_scanning = SpiralScanning(
            name=self.pattern_name,
            diameter=self.spiral_diameter,
            height=self.spiral_height,
            number_of_revolutions=self.num_revolutions,
            description=self.pattern_description,
        )
        stimulus_pattern = OptogeneticStimulusPattern(
            name=self.pattern_name,
            description=self.pattern_description,
            duration=self.duration,
            number_of_stimulus_presentation=self.number_of_stimulus_presentation,
            inter_stimulus_interval=self.inter_stimulus_interval,
            spiral_scanning=spiral_scanning,
        )
        self.nwbfile.add_lab_meta_data(stimulus_pattern)

        assert stimulus_pattern.name in self.nwbfile.lab_meta_data.keys()
        assert stimulus_pattern in self.nwbfile.lab_meta_data.values()

        stim_site = PatternedOptogeneticStimulusSite(
            name=self.site_name,
            device=self.device,
            description=self.site_description,
            excitation_lambda=self.stimulation_wavelenght,  # nm
            effector=self.effector,
            location=self.location,
        )
        self.nwbfile.add_ogen_site(stim_site)

        assert stim_site.name in self.nwbfile.ogen_sites.keys()
        assert stim_site in self.nwbfile.ogen_sites.values()

        spatial_light_modulator = SpatialLightModulator(
            name=self.slm_name,
            description=self.series_description,
            model=self.slm_model,
            resolution=self.slm_resolution,
        )
        self.nwbfile.add_device(spatial_light_modulator)
        light_source = LightSource(
            name=self.light_source_name,
            stimulation_wavelenght=self.stimulation_wavelenght,  # nm
            description=self.light_source_description,
            filter=self.filter,
            power=self.power,
            intensity=self.intensity,
            exposure_time=self.exposure_time,
            pulse_rate=self.pulse_rate,
        )
        self.nwbfile.add_device(light_source)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        photostimulation = PatternedOptogeneticSeries(
            name=self.series_name,
            description=self.series_description,
            data=data,
            unit=self.unit,
            timestamps=timestamps,
            rois=self.roi_table_region,
            stimulus_pattern=stimulus_pattern,
            site=stim_site,
            device=self.device,
            light_source=light_source,
            spatial_light_modulator=spatial_light_modulator,
        )
        assert_array_equal(photostimulation.data, data)

        self.nwbfile.add_stimulus(photostimulation)

        assert photostimulation.name in self.nwbfile.stimulus.keys()
        assert photostimulation in self.nwbfile.stimulus.values()

    def test_patterned_optogenetic_series_roundtrip_with_spiralscanning(self):
        spiral_scanning = SpiralScanning(
            name=self.pattern_name,
            diameter=self.spiral_diameter,
            height=self.spiral_height,
            number_of_revolutions=self.num_revolutions,
            description=self.pattern_description,
        )
        stimulus_pattern = OptogeneticStimulusPattern(
            name=self.pattern_name,
            description=self.pattern_description,
            duration=self.duration,
            number_of_stimulus_presentation=self.number_of_stimulus_presentation,
            inter_stimulus_interval=self.inter_stimulus_interval,
            spiral_scanning=spiral_scanning,
        )
        self.nwbfile.add_lab_meta_data(stimulus_pattern)

        assert stimulus_pattern.name in self.nwbfile.lab_meta_data.keys()
        assert stimulus_pattern in self.nwbfile.lab_meta_data.values()

        stim_site = PatternedOptogeneticStimulusSite(
            name=self.site_name,
            device=self.device,
            description=self.site_description,
            excitation_lambda=self.stimulation_wavelenght,  # nm
            effector=self.effector,
            location=self.location,
        )
        self.nwbfile.add_ogen_site(stim_site)

        assert stim_site.name in self.nwbfile.ogen_sites.keys()
        assert stim_site in self.nwbfile.ogen_sites.values()

        spatial_light_modulator = SpatialLightModulator(
            name=self.slm_name,
            description=self.series_description,
            model=self.slm_model,
            resolution=self.slm_resolution,
        )
        self.nwbfile.add_device(spatial_light_modulator)

        light_source = LightSource(
            name=self.light_source_name,
            stimulation_wavelenght=self.stimulation_wavelenght,  # nm
            description=self.light_source_description,
            filter=self.filter,
            power=self.power,
            intensity=self.intensity,
            exposure_time=self.exposure_time,
            pulse_rate=self.pulse_rate,
        )
        self.nwbfile.add_device(light_source)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        photostimulation = PatternedOptogeneticSeries(
            name=self.series_name,
            description=self.series_description,
            data=data,
            unit=self.unit,
            timestamps=timestamps,
            rois=self.roi_table_region,
            stimulus_pattern=stimulus_pattern,
            site=stim_site,
            device=self.device,
            light_source=light_source,
            spatial_light_modulator=spatial_light_modulator,
        )

        self.nwbfile.add_stimulus(photostimulation)

        nwbfile_path = self.test_dir / "test_photostimulation_nwb.nwb"
        with NWBHDF5IO(nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            nwbfile_in = io.read()
            assert self.series_name in nwbfile_in.stimulus.keys()
            assert_array_equal(nwbfile_in.stimulus[self.series_name].data, data)

            assert self.site_name in nwbfile_in.ogen_sites.keys()
            assert self.pattern_name in nwbfile_in.lab_meta_data.keys()

    def test_patterned_optogenetic_series_constructor_with_temporalfocusing(self):
        temporal_focusing = TemporalFocusing(
            name=self.temporal_focusing_name,
            description=self.pattern_description,
            lateral_point_spread_function=self.lateral_psf,
            axial_point_spread_function=self.axial_psf,
        )
        stimulus_pattern = OptogeneticStimulusPattern(
            name=self.pattern_name,
            description=self.pattern_description,
            duration=self.duration,
            number_of_stimulus_presentation=self.number_of_stimulus_presentation,
            inter_stimulus_interval=self.inter_stimulus_interval,
            temporal_focusing=temporal_focusing,
        )
        self.nwbfile.add_lab_meta_data(stimulus_pattern)

        assert stimulus_pattern.name in self.nwbfile.lab_meta_data.keys()
        assert stimulus_pattern in self.nwbfile.lab_meta_data.values()

        stim_site = PatternedOptogeneticStimulusSite(
            name=self.site_name,
            device=self.device,
            description=self.site_description,
            excitation_lambda=self.stimulation_wavelenght,  # nm
            effector=self.effector,
            location=self.location,
        )
        self.nwbfile.add_ogen_site(stim_site)

        assert stim_site.name in self.nwbfile.ogen_sites.keys()
        assert stim_site in self.nwbfile.ogen_sites.values()

        spatial_light_modulator = SpatialLightModulator(
            name=self.slm_name,
            description=self.series_description,
            model=self.slm_model,
            resolution=self.slm_resolution,
        )
        self.nwbfile.add_device(spatial_light_modulator)

        light_source = LightSource(
            name=self.light_source_name,
            stimulation_wavelenght=self.stimulation_wavelenght,  # nm
            description=self.light_source_description,
            filter=self.filter,
            power=self.power,
            intensity=self.intensity,
            exposure_time=self.exposure_time,
            pulse_rate=self.pulse_rate,
        )
        self.nwbfile.add_device(light_source)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        photostimulation = PatternedOptogeneticSeries(
            name=self.series_name,
            description=self.series_description,
            data=data,
            unit=self.unit,
            timestamps=timestamps,
            rois=self.roi_table_region,
            stimulus_pattern=stimulus_pattern,
            site=stim_site,
            device=self.device,
            light_source=light_source,
            spatial_light_modulator=spatial_light_modulator,
        )

        assert_array_equal(photostimulation.data, data)

        self.nwbfile.add_stimulus(photostimulation)

        assert photostimulation.name in self.nwbfile.stimulus.keys()
        assert photostimulation in self.nwbfile.stimulus.values()

    def test_patterned_optogenetic_series_roundtrip_with_temporalfocusing(self):
        temporal_focusing = TemporalFocusing(
            name=self.temporal_focusing_name,
            description=self.pattern_description,
            lateral_point_spread_function=self.lateral_psf,
            axial_point_spread_function=self.axial_psf,
        )
        stimulus_pattern = OptogeneticStimulusPattern(
            name=self.pattern_name,
            description=self.pattern_description,
            duration=self.duration,
            number_of_stimulus_presentation=self.number_of_stimulus_presentation,
            inter_stimulus_interval=self.inter_stimulus_interval,
            temporal_focusing=temporal_focusing,
        )
        self.nwbfile.add_lab_meta_data(stimulus_pattern)

        assert stimulus_pattern.name in self.nwbfile.lab_meta_data.keys()
        assert stimulus_pattern in self.nwbfile.lab_meta_data.values()

        stim_site = PatternedOptogeneticStimulusSite(
            name=self.site_name,
            device=self.device,
            description=self.site_description,
            excitation_lambda=self.stimulation_wavelenght,  # nm
            effector=self.effector,
            location=self.location,
        )
        self.nwbfile.add_ogen_site(stim_site)

        assert stim_site.name in self.nwbfile.ogen_sites.keys()
        assert stim_site in self.nwbfile.ogen_sites.values()

        spatial_light_modulator = SpatialLightModulator(
            name=self.slm_name,
            description=self.series_description,
            model=self.slm_model,
            resolution=self.slm_resolution,
        )
        self.nwbfile.add_device(spatial_light_modulator)

        light_source = LightSource(
            name=self.light_source_name,
            stimulation_wavelenght=self.stimulation_wavelenght,  # nm
            description=self.light_source_description,
            filter=self.filter,
            power=self.power,
            intensity=self.intensity,
            exposure_time=self.exposure_time,
            pulse_rate=self.pulse_rate,
        )
        self.nwbfile.add_device(light_source)

        data = np.random.rand(100, self.n_rois)  # ntime x nroi
        timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

        photostimulation = PatternedOptogeneticSeries(
            name=self.series_name,
            description=self.series_description,
            data=data,
            unit=self.unit,
            timestamps=timestamps,
            rois=self.roi_table_region,
            stimulus_pattern=stimulus_pattern,
            site=stim_site,
            device=self.device,
            light_source=light_source,
            spatial_light_modulator=spatial_light_modulator,
        )

        self.nwbfile.add_stimulus(photostimulation)

        nwbfile_path = self.test_dir / "test_photostimulation_nwb.nwb"
        with NWBHDF5IO(nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(nwbfile_path, mode="r") as io:
            nwbfile_in = io.read()
            assert self.series_name in nwbfile_in.stimulus.keys()
            assert_array_equal(nwbfile_in.stimulus[self.series_name].data, data)

            assert self.site_name in nwbfile_in.ogen_sites.keys()
            assert self.pattern_name in nwbfile_in.lab_meta_data.keys()