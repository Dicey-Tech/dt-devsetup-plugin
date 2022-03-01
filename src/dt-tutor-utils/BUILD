python_sources(
    name="dt_tutor_utils",
)


python_distribution(
    name="tutor-utils",
    provides=setup_py(
        name="dt-tutor-util",
        version="0.1.0",
        description="dt-tutor-util plugin for Tutor",
        entry_points={"tutor.plugin.v0": ["dt_utils = tutorutils.plugin"]},
    ),
)

# TODO Add tutor dependency
