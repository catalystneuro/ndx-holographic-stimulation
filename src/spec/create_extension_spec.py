# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An extension of for the optogenetic module to include the patterned photostimulation""",
        name="""ndx-holographic-stimulation""",
        version="""0.1.0""",
        author=list(map(str.strip, """Alessandra Trapani""".split(","))),
        contact=list(
            map(str.strip, """alessandramaria.trapani@gmail.com""".split(","))
        ),
    )

    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("Device", namespace="core")
    ns_builder.include_type("OptogeneticStimulusSite", namespace="core")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("LabMetaData", namespace="core")

    SpiralScanning = NWBGroupSpec(
        neurodata_type_def="SpiralScanning",
        neurodata_type_inc="DynamicTable",
        doc=("table of parameters defining the spiral scanning beam pattern"),
        attributes=[
            NWBAttributeSpec(
                name="diameter",
                doc="spiral diameter of each spot, in m",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="height",
                doc="spiral height of each spot, in m",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="number_of_revolutions",
                doc="number of turns within a spiral",
                dtype="int8",
            ),
        ],
    )

    TemporalFocusing = NWBGroupSpec(
        neurodata_type_def="TemporalFocusing",
        neurodata_type_inc="DynamicTable",
        doc=("table of parameters defining the temporal focusing beam-shaping"),
        attributes=[
            NWBAttributeSpec(
                name="lateral_point_spread_function",
                doc="estimated lateral spatial profile or point spread function, expressed as mean [um] ± s.d [um]",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="axial_point_spread_function",
                doc="estimated axial spatial profile or point spread function, expressed as mean [um]± s.d [um]",
                dtype="text",
            ),
        ],
    )

    OptogeneticStimulusPattern = NWBGroupSpec(
        neurodata_type_def="OptogeneticStimulusPattern",
        neurodata_type_inc="LabMetaData",
        doc=("Holographic excitation single ROI"),
        attributes=[
            NWBAttributeSpec(
                name="description",
                doc="description of the stimulus pattern",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="duration",
                doc="the time duration for a single stimulus, in sec",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="number_of_stimulus_presentation",
                doc="number of times the patterned stimulus is presented in one stimulation interval",
                dtype="int8",
            ),
            NWBAttributeSpec(
                name="inter_stimulus_interval",
                doc="duration of the interval between each individual stimulus, in sec",
                dtype="float32",
            ),
        ],
        groups=[
            NWBGroupSpec(
                name="spiral_scanning",
                neurodata_type_inc="SpiralScanning",
                doc="The spiral scanning beam pattern is obtained by scanning the beam spot following a spiral path over the somatic membrane ",
                quantity="?",
            ),
            NWBGroupSpec(
                name="temporal_focusing",
                neurodata_type_inc="TemporalFocusing",
                doc="The temporal focusing beam-shaping is accomplished by manipulating light phases to generate custom-shaped light patterns that can illuminate extended lateral regions (e.g., the entire cell body) simultaneously.",
                quantity="?",
            ),
        ]
    )



    PatternedOptogeneticStimulusSite = NWBGroupSpec(
        neurodata_type_def="PatternedOptogeneticStimulusSite",
        neurodata_type_inc="OptogeneticStimulusSite",
        doc=(
            "An extension of OptogeneticStimulusSite to include the geometrical representation for "
            "the stimulus."
        ),
        attributes=[
            NWBAttributeSpec(
                name="effector",
                doc="Light-activated effector protein expressed by the targeted cell (eg. ChR2)",
                dtype="text",
                required=False,
            ),
        ],
    )
    
    SpatialLightModulator = NWBGroupSpec(
        neurodata_type_def="SpatialLightModulator",
        neurodata_type_inc="Device",
        doc=(
            "An extension of Device to include the Spatial Light Modulator metadata"
        ),
        attributes=[
            NWBAttributeSpec(
                name="model",
                doc="model of the Spatial Light Modulator, if known",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="resolution",
                doc="resolution of the Spatial Light Modulator in um, if known",
                dtype="float32",
            ),
        ],
    )
    
    LightSource = NWBGroupSpec(
        neurodata_type_def="LightSource",
        neurodata_type_inc="Device",
        doc=(
            "An extension of Device to include the Light Sorce metadata"
        ),
        attributes=[
            NWBAttributeSpec(
                name="stimulation_wavelenght",
                doc="stimulation wavelenght in nm",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="filter",
                doc="filter", #TODO write a better doc
                dtype="text",
            ),
            NWBAttributeSpec(
                name="power",
                doc="power of the stimulation in W, if known", 
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="intensity",
                doc="intensity of the excitation in W/m^2, if known.", 
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="exposure_time",
                doc="exposure time of the sample", 
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="pulse_rate",
                doc="pulse rate of the light source, if the light source is a pulsed laser", 
                dtype="float32",
            ),
        ],
    )
    
    PatternedOptogeneticSeries = NWBGroupSpec(
        neurodata_type_def="PatternedOptogeneticSeries",
        neurodata_type_inc="TimeSeries",
        doc=(
            "An extension of OptogeneticSeries to include the spatial patterns for "
            "the photostimulation."
        ),
        attributes=[
            NWBAttributeSpec(
                name="unit",
                doc="SI unit of data",
                dtype="text",
                default_value="watts",
            ),
        ],
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc=(
                    "The data values. The first dimension must be time. The second dimension represents ROIs"
                ),
                dtype="numeric",
                shape=(None, None),
                dims=("num_times", "num_rois"),
            ),
            NWBDatasetSpec(
                name="rois",
                doc="references rows of ROI table",
                dtype="int8",
                neurodata_type_inc="DynamicTableRegion",
            ),
        ],
        links=[
            NWBLinkSpec(
                name="site",
                doc="link to the patterned stimulus site",
                target_type="PatternedOptogeneticStimulusSite",
                quantity="*",
            ),
            NWBLinkSpec(
                name="stimulus_pattern",
                doc="link to the stimulus pattern",
                target_type="OptogeneticStimulusPattern",
                quantity="*",
            ),
            NWBLinkSpec(
                name="device",
                doc="link to the device used to generate the photostimulation",
                target_type="Device",
                quantity="*",
            ),
            NWBLinkSpec(
                name="spatial_light_modulator",
                doc="link to the spatial light modulator device",
                target_type="SpatialLightModulator",
                quantity="*",
            ),
            NWBLinkSpec(
                name="light_source",
                doc="link to the light source",
                target_type="LightSource",
                quantity="*",
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
        SpiralScanning,
        TemporalFocusing,
        OptogeneticStimulusPattern,
        PatternedOptogeneticStimulusSite,
        PatternedOptogeneticSeries,
        SpatialLightModulator,
        LightSource,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "spec")
    )
    export_spec(ns_builder, new_data_types, output_dir)
    print(
        "Spec files generated. Please make sure to rerun `pip install .` to load the changes."
    )


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
