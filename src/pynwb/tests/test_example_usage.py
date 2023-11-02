def test_example_usage():
    import datetime
    import numpy as np
    from pynwb import NWBFile, NWBHDF5IO
    from ndx_holographic_stimulation import (
        HolographicSeries,
        HolographicStimulusSite,
        HolographicStimulusPattern,
    )
    from pynwb.ophys import ImageSegmentation, OpticalChannel

    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )

    device_recording = nwbfile.create_device(
        name="Microscope",
        description="My two-photon microscope",
        manufacturer="The best microscope manufacturer",
    )

    optical_channel = OpticalChannel(
        name="OpticalChannel",
        description="an optical channel",
        emission_lambda=500.0,
    )
    imaging_plane = nwbfile.create_imaging_plane(
        name="ImagingPlane",
        optical_channel=optical_channel,
        imaging_rate=30.0,
        description="a very interesting part of the brain",
        device=device_recording,
        excitation_lambda=600.0,
        indicator="GFP",
        location="V1",
        grid_spacing=[0.01, 0.01],
        grid_spacing_unit="meters",
        origin_coords=[1.0, 2.0, 3.0],
        origin_coords_unit="meters",
    )

    img_seg = ImageSegmentation()

    plane_seg = img_seg.create_plane_segmentation(
        name="PlaneSegmentation",
        description="output from segmenting my favorite imaging plane",
        imaging_plane=imaging_plane,
    )
    for _ in range(30):
        image_mask = np.zeros((100, 100))

        # randomly generate example image masks
        x = np.random.randint(0, 95)
        y = np.random.randint(0, 95)
        # define an example 4 x 3 region of pixels of weight '1'
        pixel_mask = []
        for ix in range(x, x + 4):
            for iy in range(y, y + 3):
                pixel_mask.append((ix, iy, 1))
        plane_seg.add_roi(pixel_mask=pixel_mask)

    roi_table_region = plane_seg.create_roi_table_region(
        region=[0, 1], description="the first of two ROIs"
    )

    device_stimulating = nwbfile.create_device(
        name="device",
        description="Microsope used for holography",
    )
    stimulus_pattern = HolographicStimulusPattern(
        name="spiral", description="5 revolutions, 5 repetitions"
    )
    holo_stim_site = HolographicStimulusSite(
        name="HolographicStimulusSite",
        device=device_stimulating,
        description="This is an example holographic site.",
        excitation_lambda=600.0,  # nm
        effector="ChR2",
        location="VISrl",
        stimulus_pattern=stimulus_pattern,
    )
    nwbfile.add_ogen_site(holo_stim_site)

    data = np.random.rand(100, 12)  # ntime x nroi
    timestamps = np.linspace(0, 10, num=100)  # a timestamp for every frame

    holographic_stimulation = HolographicSeries(
        name="holographic_stimulation",
        description="Holographic stimulus on 12 rois",
        data=data,
        rois=roi_table_region,
        site=holo_stim_site,
        timestamps=timestamps,
    )

    nwbfile.add_stimulus(holographic_stimulation)

    path = "test_holographic_stimulation.nwb"
    with NWBHDF5IO(path, mode="w") as io:
        io.write(nwbfile)

    with NWBHDF5IO(path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        print(read_nwbfile)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    test_example_usage()
