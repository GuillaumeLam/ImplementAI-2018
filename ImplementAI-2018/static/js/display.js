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

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
//Storing data:
myObj = httpGet(url)

//myObj = {
//    pose: "squat",
//    comment: {
//        comment1: "back is off by x degrees",
//        comment2: "blah blah blah",
//        comment3: "blah blah blah blah blah"
//    },
//    tip: {
//        tip1: "straighten back",
//        tip2: "arm angle needs to be 90 degrees",
//        tip3: "blah blah blah"
//    }
//};
myJSON = JSON.stringify(myObj);
localStorage.setItem("testJSON", myJSON);

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