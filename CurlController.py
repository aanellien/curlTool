from flask import Flask,render_template,request,jsonify
import CurlService
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('status.html')

@app.route('/visualization',methods=['POST'])
def loadVisualization():
    file = request.files['file']
    bucket = request.form['bucket_name']
    file_name = request.form['file_name']
    urn= CurlService.fullWorkFlow(bucket,file_name,file)
    if(urn[-1]=='='):
        urn= urn[:-1]

    token = CurlService.getToken(CurlService.Scope.read_viewable)
    return render_template('visualization.html',urn=urn,token=token)


@app.route('/createBucket',methods=['POST'])
def createBucket():
    bucket_name= request.json['bucket_name']
    return jsonify(CurlService.createBucket(CurlService.getToken(CurlService.Scope.create_bucket),bucket_name))

@app.route('/uploadFile',methods=['POST'])
def uploadFile():
    print str(request)
    file = request.files['file']
    bucket = request.form['bucket_name']
    file_name = request.form['file_name']
    urn = CurlService.uploadFile(CurlService.getToken(CurlService.Scope.write_data), bucket, file_name,file )
    urn = base64.b64encode(urn)
    return jsonify(urn);

@app.route('/convertFile',methods=['POST'])
def convertFile():
    urn = request.json['urn']
    return jsonify(CurlService.convertFile(CurlService.getToken(CurlService.Scope.read_write_data),urn))

@app.route('/getStatus',methods=['POST'])
def getStatus():
    urn = request.json['urn']
    status=CurlService.checkConversionStatus(CurlService.getToken(CurlService.Scope.data_read),urn)
    return jsonify(status)

@app.route('/viewImage',methods=["GET"])
def viewImage():
    urn = request.args.get('urn')
    token = CurlService.getToken(CurlService.Scope.read_viewable)
    return render_template('visualization.html',urn=urn,token=token)

if __name__ == '__main__':
   app.run(debug = True)
