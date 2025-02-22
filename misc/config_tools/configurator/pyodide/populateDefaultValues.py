#!/usr/bin/env python3
#
# Copyright (C) 2022 Intel Corporation.
#
# SPDX-License-Identifier: BSD-3-Clause
#

__package__ = 'configurator.pyodide'

from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import tostring

from scenario_config.pipeline import PipelineObject, PipelineEngine
from scenario_config.xml_loader import XMLLoadStage
from scenario_config.default_populator import DefaultValuePopulatingStage

from .pyodide import write_temp_file, nuc11_scenario, scenario_xml_schema_path, convert_result
from .loadScenario import load_scenario_xml


def main(scenario):
    pipeline = PipelineEngine(["schema_path", "scenario_path"])
    pipeline.add_stages([
        XMLLoadStage("schema"),
        XMLLoadStage("scenario"),
        DefaultValuePopulatingStage(),
    ])
    with TemporaryDirectory() as tmpdir:
        write_temp_file(tmpdir, {
            'scenario.xml': scenario
        })
        scenario_file_path = Path(tmpdir) / 'scenario.xml'

        obj = PipelineObject(
            scenario_path=scenario_file_path,
            schema_path=scenario_xml_schema_path,
        )
        pipeline.run(obj)
        result = tostring(obj.get("scenario_etree").getroot())
        result = result.decode()
    result = convert_result({
        'xml': result,
        'json': load_scenario_xml(result)
    })
    return result


def test():
    main(nuc11_scenario)


if __name__ == '__main__':
    test()
