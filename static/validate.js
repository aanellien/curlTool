var ERROR_MESSAGE = "Error occured. Excecution stopped.";

function validate() {
   var bucket_name= document.getElementsByName("bucket_name")[0].value;
  if(!bucket_name){
    alert("Please fill name of Bucket");
    return ;
  }
  var file_name = document.getElementsByName("file_name")[0].value;
  if(!file_name){
    alert("Please fill file name");
    return ;
  }
  var file= document.getElementsByName("file")[0].value;
  if(!file){
    alert("Please select file to Upload")
    return ;
  }

  createBucket(bucket_name,file_name)
};

function createBucket(bucket_name,file_name){
  status_text = $('#status_text');
  status_text.empty();
  var msg;
  $.ajax({
    url: "/createBucket",
    type: "POST",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({ "bucket_name" : bucket_name})
  }).done(function(code){
      if(code=="200"){
        msg="new bucket created";
      }
      else if(code=="409"){
        msg="bucket already exists";
      }
      else{
        msg="Problem creating bucket. Execution stopped.";
        status_text.append(msg+"</br>");
        return;
      }
      status_text.append(msg+"</br>File upload starting, this might take a while</br>");
      uploadFile(bucket_name,file_name)

  }).fail(function(){
    alert(ERROR_MESSAGE);
  });
};

function uploadFile(bucket_name,file_name){
  status_text = $('#status_text');
  var form_data = new FormData(document.forms.namedItem("fileinfo"))
  $.ajax({
    url: "/uploadFile",
    type: "POST",
    contentType: false,
    cache: false,
    processData: false,
    data: form_data
  }).done(function(urn){
    status_text.append("file uploaded with encrypted urn code: "+ urn+"</br>");
    convertFile(urn);


  }).fail(function(){
    alert(ERROR_MESSAGE);
  });
};

function convertFile(urn){
  $.ajax({
    url: "/convertFile",
    type: "POST",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({ "urn" : urn})
  }).done(function(code){
    status_text.append("file conversion started.</br> Will start pinging status</br>");
    waitUntilConvert(urn);
}).fail(function(){
  alert(ERROR_MESSAGE);
  });
};

function  waitUntilConvert(urn){
  $.ajax({
    url: "/getStatus",
    type: "POST",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({ "urn" : urn})
  }).done(function(status){
    status_text.append("status: "+status+" </br>");
    if(status!="complete"){
      waitUntilConvert(urn);
    }
    else{
      status_text.append("Redirecting to page to load visualization</br>");
      window.location.href = "/viewImage?urn="+urn;

    }
}).fail(function(){
  alert(ERROR_MESSAGE);
  });
};
