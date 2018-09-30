//import axios from 'axios';
//
var url="http://127.0.0.1:5000/improv_json";

//while(1) {
//    if(){
//
//    }
//    else {
//        axios.get(url)
//        .then(data=>)
//        .catch(err=>console.log(err))
//    }
//}

//function httpGet(theUrl)
//{
//    var xmlHttp = new XMLHttpRequest();
//    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
//    xmlHttp.send( null );
//    return xmlHttp.responseText;
//}
////Storing data:
//myObj = httpGet(url)

myObj = {
    pose: "Squat",
    comment: {
        comment1: "Back is off by 10 degrees",
        comment2: "Arm angle should be 180 degrees",
        comment3: "Knees are too slanted at 30 degrees"
    },
    tip: {
        tip1: "Straighten your back more",
        tip2: "Arms need to be straight",
        tip3: "Knees can't be more forward than your toes"
    }
};
myJSON = JSON.stringify(myObj);
localStorage.setItem("testJSON", myJSON);


//(function worker() {
//  $.ajax({
//    url: 'http://127.0.0.1:5000/improv_json',
//    success: function(data) {
//      console.log(data);
//    },
//    complete: function() {
//      setTimeout(worker, 1000);
//    }
//  });
//})();


//Retrieving data:
text = localStorage.getItem("testJSON");
obj = JSON.parse(text);
document.getElementById("pose").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.pose;
document.getElementById("comment1").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.comment.comment1;
document.getElementById("comment2").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.comment.comment2;
document.getElementById("comment3").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.comment.comment3;
document.getElementById("tip1").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.tip.tip1;
document.getElementById("tip2").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.tip.tip2;
document.getElementById("tip3").innerHTML = '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + obj.tip.tip3;