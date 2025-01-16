import autogen

initializer = autogen.UserProxyAgent(
    name="Init",
    code_execution_config={"use_docker": False},
)
