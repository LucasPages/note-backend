from django.test import TestCase
from notes.models import Note
from freezegun import freeze_time
from datetime import datetime, timezone


class NoteTest(TestCase):
    def setUp(self):
        pass

    def test_empty_note(self):
        note_obj = Note.objects.create()

        self.assertEqual(note_obj.title, "")
        self.assertEqual(note_obj.note, "")
        self.assertNotEqual(note_obj.created_at, None)
        self.assertNotEqual(note_obj.last_edited, None)
    
    @freeze_time("2024-10-12 18:17:00")
    def test_creation_date_added(self):
        note_obj = Note.objects.create()

        self.assertEqual(note_obj.created_at, datetime.now(tz=timezone.utc))

    def test_edited_correct_date(self):
        note_obj = Note.objects.create()

        note_obj.title = "test title"
        freezer = freeze_time("2024-10-12 18:17:00")
        freezer.start()
        note_obj.save()

        self.assertEqual(note_obj.last_edited, datetime.now(tz=timezone.utc))
        self.assertNotEqual(note_obj.created_at, datetime.now(tz=timezone.utc))
        freezer.stop()
    
    def test_string_representation(self):
        note_obj_20 = Note.objects.create(title="test", note="this note is a test")
        note_obj_more = Note.objects.create(title="test", note="this note is a test, and it's long")

        self.assertEqual(str(note_obj_20), f"{note_obj_20.title} : {note_obj_20.note}")
        self.assertEqual(str(note_obj_more), f"{note_obj_more.title} : {note_obj_more.note[:20]}...")
