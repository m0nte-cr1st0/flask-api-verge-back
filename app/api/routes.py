import json
import os

from flask import redirect, url_for, request, jsonify, send_file

from werkzeug.utils import secure_filename

from app.models import Application, Version
from app import app, ma, db
from app.api import bp


uploads_dir = os.path.join('/'.join(app.instance_path.split('/')[:-1]), 'uploads')


class ApplicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class ApplicationDetailSchema(ma.ModelSchema):
    class Meta:
        model = Application
        fields = ('id', 'name', 'versions')


class VersionSchema(ma.Schema):
    class Meta:
        fields = ('application_id', 'id', 'file')


class VersionDetailSchema(ma.ModelSchema):
    application = ma.Nested(ApplicationDetailSchema, only=['name'])

    class Meta:
        model = Version
        fields = ('id', 'file', 'application_id', 'application')


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)

application_detail_schema = ApplicationDetailSchema()

version_schema = VersionDetailSchema()
versions_schema = VersionSchema(many=True)


@bp.route("", methods=['GET', 'POST'])
def applications():
    if request.method == 'GET':
        result = applications_schema.dump(Application.query.all())
        return jsonify(result)

    elif request.method == 'POST':
        id = request.json.get('application_id', '')
        name = request.json.get('application_title', '')
        app = Application(id=id, name=name)
        db.session.add(app)
        db.session.commit()
        result = application_schema.dump(app)
        return jsonify(result)


@bp.route("/<id>")
def application_detail(id):
    application = Application.query.get(id)
    result = application_detail_schema.dump(application)
    return jsonify(result)


@app.route('/files/<file>/download')
def download_file(file):
    return send_file(uploads_dir+'/files/'+file, as_attachment=True, attachment_filename=file)


@bp.route("/<id>/<version_id>", methods=['GET', 'POST'])
def versions(id, version_id):
    if request.method == 'GET':
        result = version_schema.dump(Version.query.get(version_id))
        return jsonify(result)

    elif request.method == 'POST':
        version = Version(id=version_id, application_id=id)
        db.session.add(version)
        db.session.commit()
        versions = Version.query.all()
        result = versions_schema.dump(versions)
        print(999)
        return jsonify(result)


def allowed_file(filename):
    return '.' in filename


@bp.route("/<id>/<version_id>/file", methods=['POST'])
def upload_file(id, version_id):
    print(request.files)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = 'files/'+secure_filename(file.filename)
        version = Version.query.get(version_id)
        version.file = filename
        db.session.commit()
        file.save(os.path.join(uploads_dir, filename))
        return redirect(url_for('api.versions',
                                id=id, version_id=version_id))
