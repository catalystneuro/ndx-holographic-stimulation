Overview
========

.. note::
    The extension stores information about holographic stimulus across two folders in the NWB file: stimulus and general.
    In total there are 8 new data types:

    ``PatternedOptogeneticSeries`` is an extension of ``TimeSeries``. Each column contains the time series associated with the stimulus delivered to a specific ROI, referenced by ``roi_table_region`` that references the rows of the ``PlaneSegmentation``. stimulus_pattern_ids (num_times, num_rois) references the rows of ``OptogeneticStimulusPatternsTable``, in case the stimulation parameters change in time or with respect to the stimulated ROI. The series contains also links to the device used for the photostimulation, and the stimulus site.
    ``PatternedOptogeneticStimulusSite`` is an extension of ``OptogeneticStimulusSite``. It contains an additional attribute for the effector (opsin) used.
    ``OptogeneticStimulusPatternsTable`` stores all the different patterns (parameters could change in time and for each ROI)
    ``OptogeneticStimulusPattern`` stores parameters for a more generic photostimulation pattern
    ``TemporalFocusing`` stores parameters associated with the temporal focusing photostimulation pattern
    ``SpiralScanning`` stores parameters associated with the spiral scanning photostimulation pattern
    Both ``SpiralScanning`` and ``TemporalFocusing`` are subtypes of ``OptogeneticStimulusPattern``
    ``SpatialLightModulator`` store metadata about the spatial light modulator 
    ``LightSource``  store metadata about the light source.