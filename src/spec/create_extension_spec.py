# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""An extension of for the optogenetic module to include the holographic photostimulation and its different patterns""",
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
                name="spiral_duration",
                doc="time duration for a single spiral, in sec",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="spiral_diameter",
                doc="spiral diameter of each spot, in m",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="spiral_height",
                doc="spiral height of each spot, in m",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="num_revolutions",
                doc="number of turns within a spiral",
                dtype="int8",
            ),
            NWBAttributeSpec(
                name="num_spirals",
                doc="numbers of repetitions for each spiral",
                dtype="int8",
            ),
            NWBAttributeSpec(
                name="isi_spiral",
                doc="duration of the interval between each individual spiral, in sec",
                dtype="float32",
            ),
        ],
    )

    TemporalFocusing = NWBGroupSpec(
        neurodata_type_def="TemporalFocusing",
        neurodata_type_inc="DynamicTable",
        doc=("table of parameters defining the temporal focusing beam-shaping"),
        attributes=[
            NWBAttributeSpec(
                name="lateral_psf",
                doc="estimated lateral spatial profile or point spread function, expressed as mean [um] ± s.d [um]",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="axial_psf",
                doc="estimated axial spatial profile or point spread function, expressed as mean [um]± s.d [um]",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="duration",
                doc="the time duration for a single spot, in sec",
                dtype="float32",
            ),
            NWBAttributeSpec(
                name="num_repetitions",
                doc="numbers of repetitions for each spot",
                dtype="int8",
            ),
            NWBAttributeSpec(
                name="isi",
                doc="duration of the interval between each individual spot, in sec",
                dtype="float32",
            ),
        ],
    )

    HolographicStimulusPattern = NWBGroupSpec(
        neurodata_type_def="HolographicStimulusPattern",
        neurodata_type_inc="LabMetaData",
        doc=("Holographic excitation single ROI"),
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
        ],
        attributes=[
            NWBAttributeSpec(
                name="description",
                doc="description of the stimulus pattern",
                dtype="text",
            ),
        ],
    )

    HolographicStimulusSite = NWBGroupSpec(
        neurodata_type_def="HolographicStimulusSite",
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
        datasets=[
            NWBDatasetSpec(
                name="rois",
                doc="references rows of ROI table",
                dtype="int8",
                neurodata_type_inc="DynamicTableRegion",
            ),
        ],
    )

    HolographicSeries = NWBGroupSpec(
        neurodata_type_def="HolographicSeries",
        neurodata_type_inc="TimeSeries",
        doc=(
            "An extension of OptogeneticSeries to include the holographic representation for "
            "the stimulus."
        ),
        attributes=[
            NWBAttributeSpec(
                name="unit",
                doc="SI unit of data",
                dtype="text",
                default_value="watts",
            ),
            NWBAttributeSpec(
                name="stimulation_wavelenght",
                doc="stimulation wavelenght in nm",
                dtype="float",
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
        ],
        links=[
            NWBLinkSpec(
                name="site",
                doc="link to the holographic stimulus site",
                target_type="HolographicStimulusSite",
                quantity="*",
            ),
            NWBLinkSpec(
                name="stimulus_pattern",
                doc="link to the holographic stimulus pattern",
                target_type="HolographicStimulusPattern",
                quantity="?",
            ),
            NWBLinkSpec(
                name="device",
                doc="link to the device used for generate the photostimulation",
                target_type="Device",
                quantity="?",
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
        SpiralScanning,
        TemporalFocusing,
        HolographicStimulusPattern,
        HolographicStimulusSite,
        HolographicSeries,
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
