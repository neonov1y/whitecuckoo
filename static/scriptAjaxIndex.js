function instruction(property) {
	switch (property) {
		case "show":
			document.getElementById("instLinkHide").style.display = "inline";
			document.getElementById("instLinkShow").style.display = "none";

			document.getElementById("instText").style.display = "block";
			document.getElementById("instruction").style.display = "block";
			document.getElementById("instruction").style.animation = "showInst 0.5s ease-in-out forwards";
			break;
		case "hide":
			document.getElementById("instLinkHide").style.display = "none";
			document.getElementById("instLinkShow").style.display = "inline";

			document.getElementById("instText").style.display = "none";
			document.getElementById("instruction").style.animation = "hideInst 0.5s ease-in-out forwards";
			window.setTimeout(function() {document.getElementById("instruction").style.display = "none";},500);
			break;
		default:
			break;
	}
}

function request_process() {
	var file = document.getElementById("uploadFile").files[0];

	var xhttp = new XMLHttpRequest();
	var form = new FormData();

	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			var str_data = "";
			var str_type = "";
			object = JSON.parse(xhttp.responseText);

			for (var i = 0;i < object.length;i++) {
				switch (object[i].data_type) {
					case "Message":
						str_data = object[i].message;
						break;
					case "File info":
						str_data = "Name: " + object[i].name + "<br /> Type: " + object[i].type + "<br /> Size: ";
						str_data += object[i].size + "<br /> MD5: " + object[i].md5 + "<br /> Virustotal result: ";
						str_data += object[i].flag_virustotal + "<br /> Malware description: " + object[i].virus_array;
						break;
					case "Signature":
						str_data = "Description: " + object[i].description;
						break;
					case "DNS connection":
						str_data = "Type: " + object[i].type + "<br /> DNS request: " + object[i].request + "<br /> DNS answer: " + object[i].answer;
						break;
					case "HTTP connection":
						str_data = "URL: " + object[i].url + "<br /> Host: " + object[i].host;
						break;
					case "TCP connection":
						str_data = "Source: " + object[i].source + "<br /> Destination: " + object[i].destination;
						break;
					case "UDP connection":
						str_data = "Source: " + object[i].source + "<br /> Destination: " + object[i].destination;
						break;
					case "Process":
						str_data = "Name: " + object[i].process_name;
						break;
					case "DLL loaded":
						str_data = "Name: " + mark_word_list(object[i].full_path);
						break;
					case "Command line":
						str_data = "Command: " + object[i].command;
						break;
					case "Dropped file":
						str_data = "Size: " + object[i].size + "<br /> Process which drop the file: " + object[i].process;
						str_data += "<br /> Type: " + object[i].type + "<br /> File path: " + object[i].path;
						break;
					case "Opened file":
						str_data = "File path: " + object[i].full_path;
						break;
					case "Created file":
						str_data = "File path: " + object[i].full_path;
						break;
					case "Copied file":
						str_data = "File path: " + object[i].full_path;
						break;
					case "Written file":
						str_data = "File path: " + object[i].full_path;
						break;
					case "Deleted file":
						str_data = "File path: " + object[i].full_path;
						break;
					case "Created folder":
						str_data = "Folder path: " + object[i].full_path;
						break;
					case "Deleted folder":
						str_data = "Folder path: " + object[i].full_path;
						break;
					case "Opened registry":
						str_data = "Registry path: " + mark_word_list(object[i].full_path);
						break;
					case "Readed registry":
						str_data = "Registry path: " + mark_word_list(object[i].full_path);
						break;
					case "Written registry":
						str_data = "Registry path: " + mark_word_list(object[i].full_path);
						break;
					case "Deleted registry":
						str_data = "Registry path: " + mark_word_list(object[i].full_path);
						break;
				}

				str_type = object[i].data_type;
				add_message_block(str_type, str_data);
			}
			// Loading off
			loading(0);
		}
	}

	if (file.size/1024/1024 < 20) {
		form.append("function_type", "file_check");
		form.append("file", file);
		form.append("memory_dump", document.getElementById("memoryDump").checked);
		xhttp.open("POST", document.location.origin + "/upload_process", true);
		xhttp.send(form);

		// Loading on
		loading(1);

		// Properties reset
		document.getElementById("memoryDump").checked = false;
	}
	else {
		document.getElementById("uploadBlock").innerHTML = "";
		add_message_block("Message", "File to much big, maximal size is 10M. File size: " + (file.size/1024/1024).toFixed(2).toString() + "M");
	}
}

function loading(switch_var) {
	switch (switch_var) {
		case 1:
			document.getElementById("uploadBlock").innerHTML = "";
			document.getElementById("uploadProperties").style.display = "none";
			document.getElementById("loaderSpinner").style.display = "block";
			document.getElementById("loaderText").style.display = "block";
			document.getElementById("marker").innerHTML = "";
			break;
		case 0:
			document.getElementById("uploadProperties").style.display = "block";
			document.getElementById("loaderSpinner").style.display = "none";
			document.getElementById("loaderText").style.display = "none";
			document.getElementById("generateReportButton").style.display = "inline-block";
			document.getElementById("markWordList").style.display = "inline-block";
			break;
	}
}

function add_message_block(str_type, str_data) {
	var str_color = "";
	switch (str_type) {
		case "Message":
			str_color = "#FF4500";
			break;
		case "File info":
			str_color = "#000000";
			break;
		case "Signature":
			str_color = "#E060A0";
			break;
		case "DNS connection":
			str_color = "#30B030"; // FF6383
		case "HTTP connection":
			str_color = "#30B030";
		case "TCP connection":
			str_color = "#30B030";
		case "UDP connection":
			str_color = "#30B030";
			break;
		case "Process":
			str_color = "#444444"; // 4BC0C0
			break;
		case "DLL loaded":
			str_color = "#D0A020";
			break;
		case "Command line":
			str_color = "#777777";
			break;
		case "Dropped file":
			str_color = "#1E90FF"; // FF9F40
		case "Opened file":
			str_color = "#1E90FF";
		case "Created file":
			str_color = "#1E90FF";
		case "Copied file":
			str_color = "#1E90FF";
		case "Written file":
			str_color = "#1E90FF";
		case "Deleted file":
			str_color = "#1E90FF";
		case "Created folder":
			str_color = "#1E90FF";
		case "Deleted folder":
			str_color = "#1E90FF";
			break;
		case "Opened registry":
			str_color = "#FF1493"; // FFCD56
		case "Readed registry":
			str_color = "#FF1493";
		case "Written registry":
			str_color = "#FF1493";
		case "Deleted registry":
			str_color = "#FF1493";
			break;
	}

	document.getElementById("uploadBlock").innerHTML += "\
		<div class='messageContainer' style='border-color: " + str_color + ";'>\
			<div class='typeContainer'>\
				<p class='messageType' style='color: " + str_color + "'>" + str_type + "</p>\
			</div>\
			<div class='dataContainer'>\
				<p class='messageData' style='color: " + str_color + "'>" + str_data + "</p>\
			</div>\
		</div>";
}

function generate_report() {
	var initial_code = "\
		<!DOCTYPE html>\
		<html lang='en'>\
			<head>\
				<title>Report</title>\
				<meta charset='UTF-8' />\
				<style>\
					@import url('https://fonts.googleapis.com/css?family=Open+Sans');\
					\
					.messageContainer {\
						display: block;\
						margin-top: 5px;\
						padding: 4px;\
					    padding-left: 15px;\
					    padding-right: 15px;\
						border: 1px;\
						border-style: solid;\
						border-color: #444444;\
					}\
					\
					.messageContainer:hover {\
						background-color: #E7E6E1;\
					}\
					\
					.typeContainer {\
						width: 20%;\
						max-width: 120px;\
						display: inline-block;\
						vertical-align: top;\
					}\
					\
					.dataContainer {\
						width: 75%;\
						display: inline-block;\
						vertical-align: top;\
					}\
					\
					.messageType {\
						color: #393232;\
						display: inline;\
						font-family: 'Open Sans', sans-serif;\
						font-size: 13px;\
						font-weight: bold;\
						margin-right: 10px;\
						word-wrap: break-word;\
					}\
					\
					.messageData {\
						color: #444444;\
						display: inline;\
						font-family: 'Open Sans', sans-serif;\
						font-size: 12px;\
						word-wrap: break-word;\
					}\
					\
					.markSus {\
						color: unset;\
						background-color: unset;\
					}\
					\
					" + document.getElementById("marker").innerHTML + "\
				</style>\
			</head>\
			<body>"

    var pom = document.createElement('a');
    pom.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(initial_code) + 
    	encodeURIComponent(document.getElementById("uploadBlock").innerHTML) + "</body></html>");
    pom.setAttribute("download", "report.html");

    if (document.createEvent) {
        var event = document.createEvent("MouseEvents");
        event.initEvent("click", true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function mark_word_list(str) {
	var word_list = ["dns", "tcp", "http", "udp", "root", "crypt", "cryptography", "browser", "firefox", "chrome", "opera", "safari", "iexplore", "autorun", "password"];
	var temp1 = 0, temp2, temp3, temp4, temp5, temp6, stat1, result;
	result = str

	for (var i = word_list.length - 1; i >= 0; i--) {
		stat1 = RegExp(word_list[i], "i");
		temp1 = result.search(stat1);

		while(temp1 != -1) {
			temp2 = result.slice(temp1, result.length);
			temp4 = mark_word_list_one(temp2, word_list[i]);
			temp3 = result.slice(0, temp1);
			result = temp3 + temp4;
			temp5 = result.slice(temp1 + 22 + word_list[i].length + 7, result.length);
			temp6 = temp1;
			temp1 = temp5.search(stat1);
			if(temp1 != -1) temp1 = temp1 + temp6 + 22 + word_list[i].length + 7;
			if(temp1 > 2000) break;
		}
	}
	return result
}
	

function mark_word_list_one(str, word) {
	var temp1 = 0, temp2, stat1;

	stat1 = RegExp(word, "i");
	temp1 = str.search(stat1);
	temp2 = str.slice(temp1, temp1 + word.length);
	str = str.replace(stat1, "<mark class='markSus'>" + temp2 + "</mark>");

	return str
}

function set_marker_color() {
	document.getElementById("marker").innerHTML = ".markSus {background-color: #FFFF00; color: black;}"
}