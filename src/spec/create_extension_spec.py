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
        author=list(map(str.strip, """Alessandra Trapani""".split(','))),
        contact=list(map(str.strip, """alessandramaria.trapani@gmail.com""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found.
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types.
    # all types included or used by the types specified here will also be
    # included.
    ns_builder.include_type('OptogeneticSeries', namespace='core')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    holographic_series = NWBGroupSpec(
        neurodata_type_def='HolographicSeries',
        neurodata_type_inc='OptogeneticSeries',
        doc=('An extension of OptogeneticSeries to include the geometrical representation for '
             'the stimulus.'),
        datasets=[
            NWBDatasetSpec(
                name='data',
                doc='The data values. May be 1D or 2D. The first dimension must be time. The optional second dimension represents ROIs',
                shape=(None,None),
            )
        ],
        groups=[
            NWBGroupSpec(
                name="rois",
                neurodata_type_inc="DynamicTableRegion",
                doc="a table region corresponding to the ROIs that were stimulated following data",
            )
        ]
    # TODO: add attributes

    )

    # TODO: add all of your new data types to this list
    new_data_types = [holographic_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
