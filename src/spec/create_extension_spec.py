# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""My NWB extension""",
        name="""ndx-holographic-stimulation""",
        version="""0.1.0""",
        author=list(map(str.strip, """Alessandra Trapani""".split(","))),
        contact=list(
            map(str.strip, """alessandramaria.trapani@gmail.com""".split(","))
        ),
    )

    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("OptogeneticStimulusSite", namespace="core")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("LabMetaData", namespace="core")

    HolographicStimulusPattern = NWBGroupSpec(
        neurodata_type_def="HolographicStimulusPattern",
        neurodata_type_inc="LabMetaData",
        name="HolographicStimulusPattern",
        doc=("Excitation pattern of a single ROI."),
        # TODO add the appropriate data that describe the stimulus pattern e.g. for spiral scanning we will need to define
        # spiral_duration/repetition_frequency/revolution while for temporal focusing we will need to define
        # Optical lateral PSF/Optical axial PSF related paramenters
    )

    HolographicStimulusSite = NWBGroupSpec(
        neurodata_type_def="HolographicStimulusSite",
        neurodata_type_inc="OptogeneticStimulusSite",
        doc=(
            "An extension of OptogeneticStimulusSite to include the geometrical representation for "
            "the stimulus."
        ),
    )
    HolographicStimulusSite.add_attribute(
        name="effector",
        doc="Light-activated effector protein expressed by the targeted cell (eg. ChR2)",
        dtype="text",
        required=False,
    )
    HolographicStimulusSite.add_link(
        name="stimulus_pattern",
        doc="link to the holographic stimulus pattern",
        target_type="HolographicStimulusPattern",
        quantity="?",
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
                default_value="W",
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc=(
                    "The data values. May be 1D or 2D. The first dimension must be time. The optional second dimension represents ROIs"
                ),
                dtype="numeric",
                shape=(None, None),
                dims=("num_times", "num_rois"),
            ),
            NWBDatasetSpec(
                name="rois",
                doc="references rows of ROI table",
                dtype="int",
                neurodata_type_inc="DynamicTableRegion",
            ),
        ],
        links=[
            NWBLinkSpec(
                name="site",
                doc="link to the holographic stimulus site",
                target_type="HolographicStimulusSite",
                quantity="*",
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
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
