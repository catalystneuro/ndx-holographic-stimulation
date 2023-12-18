import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_holographic_stimulation_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-holographic-stimulation.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_holographic_stimulation_specpath):
    ndx_holographic_stimulation_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-holographic-stimulation.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_holographic_stimulation_specpath)

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package level
PatternedOptogeneticSeries = get_class('PatternedOptogeneticSeries', 'ndx-holographic-stimulation')
OptogeneticStimulusPattern = get_class('OptogeneticStimulusPattern', 'ndx-holographic-stimulation')
PatternedOptogeneticStimulusSite = get_class('PatternedOptogeneticStimulusSite', 'ndx-holographic-stimulation')
SpiralScanning = get_class('SpiralScanning', 'ndx-holographic-stimulation')
TemporalFocusing = get_class('TemporalFocusing', 'ndx-holographic-stimulation')
SpatialLightModulator = get_class('SpatialLightModulator', 'ndx-holographic-stimulation')
LightSource = get_class('LightSource', 'ndx-holographic-stimulation')