from hdmf.utils import docval, popargs, get_docval, call_docval_func, AllowPositional

from pynwb import register_class, TimeSeries
from pynwb.core import NWBContainer
from pynwb.ogen import OptogeneticSeries, OptogeneticStimulusSite
from hdmf.common import DynamicTableRegion


@register_class("HolographicSeries", "ndx-holographic-stimulation")
class HolographicSeries(OptogeneticSeries):
    """
    An extension of OptogeneticSeries to include the stimulation spatial pattern and the targeted ROIs.
    """  # TODO

    # __clsconf__ = [
    #     {
    #         'add': 'add_holographic_stimulation_series',
    #         'get': 'get_holographic_stimulation_series',
    #         'create': 'create_holographic_stimulation_series',
    #         'type': HolographicSeries,
    #         'attr': 'holographic_stimulation_series'
    #     },
    # ]

    __nwbfields__ = ("site", "rois")

    @docval(
        {
            "name": "name",
            "type": str,
            "doc": ("Name of this HolographicSeries"),
        },  # required
        {
            "name": "data",
            "type": ("array_data", "data", TimeSeries),
            "shape": (None, None),  # required
            "doc": (
                "The data values in W. May be 1D or 2D. The first dimension must be time. The optional second dimension represents ROIs"
            ),
        },
        {
            "name": "site",
            "type": NWBContainer,  # required
            "doc": "The site to which this stimulus was applied.",
        },
        {
            "name": "rois",
            "type": DynamicTableRegion,  # required
            "doc": "a table region corresponding to the ROIs that were used to generate this data",
        },
        *get_docval(
            OptogeneticSeries.__init__,
            "resolution",
            "conversion",
            "timestamps",
            "starting_time",
            "rate",
            "comments",
            "description",
            "control",
            "control_description",
            "offset",
        ),
        allow_positional=AllowPositional.ERROR  # What is this for?
    )
    def __init__(self, **kwargs):
        """Construct a new HolographicSeries representing holographic stimulus"""
        data, name, site, rois = popargs("site", "rois", kwargs)
        call_docval_func(super().__init__, kwargs)
        self.name = name
        self.data = data
        self.site = site
        self.rois = rois


@register_class("HolographicStimulusSite", "ndx-holographic-stimulation")
class HolographicStimulusSite(OptogeneticStimulusSite):
    """
    Holographic optogenetic stimulus site.
    """

    __nwbfields__ = ("effector", "stimulus_pattern")

    @docval(
        {
            "name": "effector",
            "type": str,
            "doc": (
                "Light-activated effector protein expressed by the targeted cell (eg. ChR2)"
            ),
            "default": None,
        },
        {
            "name": "stimulus_pattern",
            "type": NWBContainer,
            "doc": (
                'The beam pattern on single cells, e.g. "spiral" or "temporal focusing"'
            ),
            "default": None,
        },
        *get_docval(
            OptogeneticStimulusSite.__init__,
            "name",
            "device",
            "description",
            "excitation_lambda",
            "location",
        ),
        allow_positional=AllowPositional.ERROR
    )
    def __init__(self, **kwargs):
        stimulus_pattern, effector = popargs("stimulus_pattern", "effector", kwargs)
        call_docval_func(super().__init__, kwargs)
        self.stimulus_pattern = stimulus_pattern
        self.effector = effector


@register_class("HolographicStimulusPattern", "ndx-holographic-stimulation")
class HolographicStimulusPattern(NWBContainer):
    """
    The beam pattern on single cells, e.g. "spiral" or "temporal focusing"
    """

    __nwbfields__ = "description"

    @docval(
        {
            "name": "description",
            "type": str,
            "doc": ("Human-readable description of the stimulation pattern"),
            "default": None,
        },
        *get_docval(
            NWBContainer.__init__,
            "name",
        ),
        allow_positional=AllowPositional.ERROR
    )
    def __init__(self, **kwargs):
        description = popargs("description", kwargs)
        call_docval_func(super().__init__, kwargs)
        self.description = description
