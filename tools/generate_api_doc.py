#!/bin/bash

export PYTHONPATH=src

(pydoc-markdown -m dia_parser/parse -m dia_parser/diagram -m dia_parser/obj -m dia_parser/layer -m dia_parser/attributes '{
    renderer: {
      type: markdown,
      descriptive_class_title: false,
      render_toc: true,
    }
}') > docs/API.md
