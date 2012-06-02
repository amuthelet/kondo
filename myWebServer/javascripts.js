/**
 * Created by PyCharm.
 * User: amuthelet
 * Date: 12/14/11
 * Time: 3:43 PM
 * To change this template use File | Settings | File Templates.
 */

CMD_PLAY_MOTION = 1;
CMD_READ_BATTERY = 0;
CMD_SET_VIDEO = 2;

//Browser Support Code
function CreateAjaxRequest()
{
    var ajaxRequest;  // The variable that makes Ajax possible!
    try{
        // Opera 8.0+, Firefox, Safari
        ajaxRequest = new XMLHttpRequest();
    } catch (e){
        // Internet Explorer Browsers
        try{
            ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try{
                ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e){
                // Something went wrong
                alert("Your browser broke!");
                return false;
            }
        }
    }
    return ajaxRequest;
}

// Command
function KondoAction(cmd, arg, out){
    //out = typeof(out) != 'undefined' ? out : document.getElementById('header').innerHTML;
    ajaxRequest = CreateAjaxRequest();
    // Create a function that will receive data sent from the server
    ajaxRequest.onreadystatechange = function(){
        if(ajaxRequest.readyState == 4)
        {
            if(cmd == CMD_SET_VIDEO)
                out.src = ajaxRequest.responseText;
            else if(cmd == CMD_READ_BATTERY)
                out.innerHTML = ajaxRequest.responseText;
            return ajaxRequest.responseText;
        }
    }
 
    params = "arg=" + arg + "&command=" + cmd;
    ajaxRequest.open("POST", "index.html", true);
    ajaxRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    ajaxRequest.setRequestHeader("Content-length", params.length);
    ajaxRequest.setRequestHeader("Connection", "close");

    ajaxRequest.send(params);

}

setInterval('KondoAction(CMD_READ_BATTERY,0, document.getElementById("header"))',10000);
