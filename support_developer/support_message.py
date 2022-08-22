from typing import List, Optional
import json
import traceback
import os


def support_message(
    package_name: str,
    developer_name: str,
    github_handle: str,
    image_url: str,
    repository_name: Optional[str] = None,
    expected_stack_trace_depth: int = 2,
    number_of_imports: List[int] = (5, 100, 1000, 5000)
):
    """Displays a banner asking user to support developer.
    
    Parameters
    --------------
    package_name: str
        Name of the package to ask support for.
    developer_name: str
        Name of the developer to display.
    github_handle: str
        GitHub handle of the developer.
    repository_name: Optional[str] = None
        Repository GitHub to link.
    image_url: str
        Link to an image of interest to display.
    expected_stack_trace_depth: int = 2
        Expected stack trace that must be matched to 
        display this banner.
    number_of_imports: List[int] = (5, 100, 1000)
        Import cases where we should display this banner.
    """
    if repository_name is None:
        repository_name = package_name

    stack_trace = traceback.extract_stack()

    # If the stack trace depth is not even
    # up to the expected stack trace, we stop.
    if len(stack_trace) < expected_stack_trace_depth + 1:
        return
    
    # We get the file name of the document
    # of the given level of stack trace.
    filename = stack_trace[expected_stack_trace_depth].filename

    # We check whether this is in a Jupyter Notebook.
    # That is, the package was DIRECTLY IMPORTED in
    # a Jupyter Notebook, as we do not want to see such
    # a banner chain-loaded.
    # If this is not one, we stop.
    if not filename.endswith("ipykernel_launcher.py"):
        return None

    from IPython.display import HTML, display

    # Path where to store the loading counts
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "metadata.json"
    )
    
    # We check how many times this package was already
    # imported by this user.
    if os.path.exists(path):
        with open(path, "r") as f:
            metadata = json.load(f)
    else:
        metadata = dict()

    metadata[package_name] = metadata.get(package_name, 0) + 1

    with open(path, "w") as f:
        json.dump(metadata, f)

    # If this is not one of those import cases where we expect
    # to show this banner, we skip forward.
    if metadata[package_name] not in number_of_imports:
        return

    if metadata[package_name] > number_of_imports[0]:
        long_time_user_message = """
        <span>I hope my work has saved you some time!</span><br/>
        """
    else:
        long_time_user_message=""

    display(HTML(
        """
        <style>
            .support_message_main_box {{
                position: relative;
                display: table-cell;
                vertical-align: middle;
                width: 100%;
                height: 10em;
                padding: 1em;
                padding-left: 11em;
                background-color: #f7f7f7;
                border: 1px solid #cfcfcf;
                border-radius: 2px;
            }}
            .support_message_main_box img {{
                position: absolute;
                height: 9em;
                width: 9em;
                left: 0.5em;
                top: 0.5em;
                border-radius: 1em;
            }}
        </style>
        <div class="support_message_main_box">
            <img src="{image_url}" />
            <p>
            <b>Hi!</b><br/>
            <span>I am the author of
            <a href="https://github.com/{github_handle}/{repository_name}" target="_blank">
                {package_name}
            </a>, which you use in this Notebook.
            </span><br/>
            {long_time_user}
            <span>I love to code, but I also need coffee.</span>
            <a href="https://github.com/sponsors/{github_handle}" target="_blank">
                Please sponsor me on GitHub ❤️
            </a><br/>
            <i>Good luck in your coding 🍀!</i>
            <br/>
            <i>- {developer_name}</i>
            </p>
        <div>
        """.format(
            developer_name=developer_name,
            package_name=package_name,
            repository_name=repository_name,
            image_url=image_url,
            long_time_user=long_time_user_message,
            github_handle=github_handle
        )
    ))