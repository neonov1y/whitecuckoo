function menu(link) {
	switch (link) {
		case 1:
			document.getElementById("art1").style.display = "block";
			document.getElementById("art2").style.display = "none";
			document.getElementById("art3").style.display = "none";
			break;
		case 2:
			document.getElementById("art1").style.display = "none";
			document.getElementById("art2").style.display = "block";
			document.getElementById("art3").style.display = "none";
			break;
		case 3:
			document.getElementById("art1").style.display = "none";
			document.getElementById("art2").style.display = "none";
			document.getElementById("art3").style.display = "block";
			break;
		default:
			break;
	}
}

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

function upload_report() {
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
						str_data = "name: " + object[i].name + "<br /> type: " + object[i].type + "<br /> size: ";
						str_data += object[i].size + "<br /> md5: " + object[i].md5 + "<br /> virustotal flag: ";
						str_data += object[i].flag_virustotal;
						break;
					case "Signature":
						str_data = "description: " + object[i].description;
						break;
					case "DNS connection":
						str_data = "type: " + object[i].type + "<br /> request: " + object[i].request;
						break;
					case "HTTP connection":
						str_data = "url: " + object[i].url + "<br /> host: " + object[i].host;
						break;
					case "TCP connection":
						str_data = "source: " + object[i].source + "<br /> destination: " + object[i].destination;
						break;
					case "UDP connection":
						str_data = "source: " + object[i].source + "<br /> destination: " + object[i].destination;
						break;
					case "Process":
						str_data = "name: " + object[i].process_name;
						break;
					case "DLL loaded":
						str_data = "full_path: " + object[i].full_path;
						break;
					case "Command line":
						str_data = "full_path: " + object[i].command;
						break;
					case "Dropped file":
						str_data = "size: " + object[i].size + "<br /> process: " + object[i].process;
						str_data += "<br /> type: " + object[i].type + "<br /> path: " + object[i].path;
						break;
					case "Opened file":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Created file":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Copied file":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Written file":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Deleted file":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Created folder":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Deleted folder":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Opened registry":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Readed registry":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Written registry":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
					case "Deleted registry":
						str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
						break;
				}

				str_type = object[i].data_type;

				if (i == 0) add_message_block("Message", "New data detected.");

				add_message_block(str_type, str_data);
			}

			if (i == 0) add_message_block("Message", "New data not detected.");

			// Loading off
			document.getElementById("uploadProperties").style.display = "inline-block";
			document.getElementById("loaderSpinner").style.display = "none";
			document.getElementById("loaderText").style.display = "none";
		}
	}

	// File send if size is valid
	if (file.size/1024/1024 < 10) {
		form.append("file", file);
		xhttp.open("POST", document.location.href + "file_upload", true);
		xhttp.send(form);

		// Loading on
		document.getElementById("uploadBlock").innerHTML = "";
		document.getElementById("uploadProperties").style.display = "none";
		document.getElementById("loaderSpinner").style.display = "block";
		document.getElementById("loaderText").style.display = "block";

		// Properties reset
		document.getElementById("scanTime").value = "";
		document.getElementById("memoryDump").checked = false;
	}
	else {
		document.getElementById("uploadBlock").innerHTML = "";
		add_message_block("Message", "File to much big, maximal size is 10M. File size: " + (file.size/1024/1024).toFixed(2).toString() + "M");
	}
}

function upload_file() {

}

function add_message_block(str_type, str_data) {
	var str_color = "";
	switch (str_type) {
		case "Message":
			str_color = "#FF4500";
			break;
		case "File info":
			str_color = "#CD853F";
			break;
		case "Signature":
			str_color = "#FF69B4";
			break;
		case "DNS connection":
			str_color = "#32CD32"; // FF6383
		case "HTTP connection":
			str_color = "#32CD32";
		case "TCP connection":
			str_color = "#32CD32";
		case "UDP connection":
			str_color = "#32CD32";
			break;
		case "Process":
			str_color = "#4BC0C0"; // 4BC0C0
			break;
		case "DLL loaded":
			str_color = "#DAA520";
			break;
		case "Command line":
			str_color = "#696969";
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