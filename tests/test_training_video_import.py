import unittest

from ml.training_video_import import scene_scenario


class TrainingSceneScenarioTests(unittest.TestCase):
    def test_official_scenario_survives_arbitrary_producer_scene_name(self):
        for number in range(1, 9):
            scenario = f'S{number:02d}'
            with self.subTest(scenario=scenario):
                self.assertEqual(scene_scenario({'scene_id': 'factory-camera-clip',
                    'scenario_id': scenario, 'official_scenario': scenario}), scenario)

    def test_existing_and_lowercase_scene_ids_keep_their_direction(self):
        examples = {'ur-fall-03-cam0': 'S07', 's07-new-subject4-fall-16': 'S07',
                    'S07_urfall01': 'S07', 's02-new-mendeley-3_te8': 'S02',
                    's04-smoke-full': 'S04'}
        for name, scenario in examples.items():
            with self.subTest(scene=name):
                self.assertEqual(scene_scenario({'scene_id': name}), scenario)

    def test_unknown_or_conflicting_metadata_is_not_silently_labelled_fire(self):
        examples = [
            {'scene_id': 'factory-camera-clip'},
            {'scene_id': 'S02_factory', 'scenario_id': 'S02', 'official_scenario': 'S04'},
            {'scene_id': 'S07_fall', 'scenario_id': 'fall'},
            {'scene_id': 'S07_fall', 'scenario_id': ['S07']},
            {'scene_id': 'S08unseparated'},
        ]
        for entry in examples:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                scene_scenario(entry)


if __name__ == '__main__':
    unittest.main()
