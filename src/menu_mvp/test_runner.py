from pathlib import Path

from django.test.runner import DiscoverRunner

SRC_DIR = str(Path(__file__).resolve().parent.parent)


class SrcLayoutDiscoverRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, **kwargs):
        if not test_labels:
            test_labels = [SRC_DIR]
        return super().build_suite(test_labels, **kwargs)