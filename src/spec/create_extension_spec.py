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
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("OptogeneticSeries", namespace="core")
    ns_builder.include_type("ImagingPlane", namespace="core")
    ns_builder.include_type("OptogeneticStimulusSite", namespace="core")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")

    HolographicStimulusPattern = NWBGroupSpec(
        neurodata_type_def="HolographicStimulusPattern",
        neurodata_type_inc="DynamicTable",
        doc=("Excitation pattern of a single ROI."),
        # TODO add atributes that describe the stimulus pattern e.g. for spiral scanning we will need to define
        # spiral_duration/repetition_frequency/revolution while for temporal focusing we will need to define
        # Optical lateral PSF/Optical axial PSF related paramenters
    )

    HolographicStimulationTarget = NWBGroupSpec(
        neurodata_type_def="HolographicStimulationTarget",
        neurodata_type_inc="ImagingPlane",
        doc=(
            "An extension of ImagingPlane to include the metadata for the holographic stimulation."
        ),
    )
    HolographicStimulationTarget.add_attribute(
        name="effector",
        doc="the opsin (membrane channel) used to write neural activity",
        dtype="text",
        required=False,
    )

    HolographicStimulusSite = NWBGroupSpec(
        neurodata_type_def="HolographicStimulusSite",
        neurodata_type_inc="OptogeneticStimulusSite",
        doc=(
            "An extension of OptogeneticStimulusSite to include the geometrical representation for "
            "the stimulus."
        ),
    )
    HolographicStimulusSite.add_link(
        doc="link to the holographic stimulus pattern",
        target_type="HolographicStimulusPattern",
        quantity="?",
    )
    HolographicStimulusSite.add_link(
        doc="link to the holographic target",
        target_type="HolographicStimulationTarget",
        quantity="?",
    )

    HolographicSeries = NWBGroupSpec(
        neurodata_type_def="HolographicSeries",
        neurodata_type_inc="OptogeneticSeries",
        doc=(
            "An extension of OptogeneticSeries to include the holographic representation for "
            "the stimulus."
        ),
    )
    HolographicSeries.add_dataset(
        name='data',
        doc="The data values. May be 1D or 2D. The first dimension must be time. The optional second dimension represents ROIs",
        shape=(None, None),
        dtype="float",
        quantity="?",
    )
    HolographicSeries.add_attribute(
        name="unit",
        doc="The base unit of measurement (should be SI unit - default W)",
        dtype="text",
        required=False,
    )
    HolographicSeries.add_link(
        name='rois',
        doc="link to the stimulated rois",
        target_type="DynamicTableRegion",
        quantity="?",
    )
    HolographicSeries.add_link(
        name='site',
        doc="link to the holographic stimulus site",
        target_type="HolographicStimulusSite",
        quantity="?",
    )


    # TODO: add all of your new data types to this list
    new_data_types = [
        HolographicStimulusPattern,
        HolographicStimulationTarget,
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
