from flask import Flask, g

import pkg_resources

from commitmentscheme.api.blueprints import cs_bp

__all__ = ['commitmentscheme']

# create the app
commitmentscheme = Flask(__name__)

# load the application configuration
config = pkg_resources.resource_filename(
    "commitmentscheme.api.config", "default.cfg")
commitmentscheme.config.from_pyfile(config)

# register blueprints
commitmentscheme.register_blueprint(cs_bp)


if __name__ == "__main__":
    api_host = commitmentscheme.config.get("API_HOST")
    api_port = commitmentscheme.config.get("API_PORT")
    api_debug = commitmentscheme.config.get("API_DEBUG")
    commitmentscheme.run(host=api_host,
                     port=api_port,
                     debug=api_debug,
                     use_debugger=api_debug)
