# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FlaggedContent'
        db.create_table('flag_flaggedcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flagged_content', to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='moderated_content', null=True, to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('flag', ['FlaggedContent'])

        # Adding unique constraint on 'FlaggedContent', fields ['content_type', 'object_id']
        db.create_unique('flag_flaggedcontent', ['content_type_id', 'object_id'])

        # Adding model 'FlagInstance'
        db.create_table('flag_flaginstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flagged_content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flag.FlaggedContent'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('when_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('when_recalled', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('flag', ['FlagInstance'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FlaggedContent', fields ['content_type', 'object_id']
        db.delete_unique('flag_flaggedcontent', ['content_type_id', 'object_id'])

        # Deleting model 'FlaggedContent'
        db.delete_table('flag_flaggedcontent')

        # Deleting model 'FlagInstance'
        db.delete_table('flag_flaginstance')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flag.flaggedcontent': {
            'Meta': {'unique_together': "[('content_type', 'object_id')]", 'object_name': 'FlaggedContent'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flagged_content'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderated_content'", 'null': 'True', 'to': "orm['auth.User']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'})
        },
        'flag.flaginstance': {
            'Meta': {'object_name': 'FlagInstance'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'flagged_content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flag.FlaggedContent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'when_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'when_recalled': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['flag']
