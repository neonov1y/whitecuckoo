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
				if (object[i].data_type == "DNS connection") {
					str_data = "type: " + object[i].type + "<br /> request: " + object[i].request;
					str_type = "DNS connection: ";
				}
				else if (object[i].data_type == "HTTP connection") {
					str_data = "url: " + object[i].url + "<br /> host: " + object[i].host;
					str_type = "HTTP connection: ";
				}
				else if (object[i].data_type == "TCP connection") {
					str_data = "source: " + object[i].source + "<br /> destination: " + object[i].destination;
					str_type = "TCP connection: ";
				}
				else if (object[i].data_type == "UDP connection") {
					str_data = "source: " + object[i].source + "<br /> destination: " + object[i].destination;
					str_type = "UDP connection: ";
				}
				else if (object[i].data_type == "Process") {
					str_data = "name: " + object[i].process_name;
					str_type = "Process: ";
				}
				else if (object[i].data_type == "Dropped file") {
					str_data = "size: " + object[i].size + "<br /> process: " + object[i].process;
					str_data += "<br /> type: " + object[i].type + "<br /> path: " + object[i].path;
					str_type = "Dropped file: ";
				}
				else if (object[i].data_type == "Deleted file") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Deleted file: ";
				}
				else if (object[i].data_type == "Created file") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Created file: ";
				}
				else if (object[i].data_type == "Created folder") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Created folder: ";
				}
				else if (object[i].data_type == "Deleted folder") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Deleted folder: ";
				}
				else if (object[i].data_type == "Written registry") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Written registry: ";
				}
				else if (object[i].data_type == "Opened registry") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Opened registry: ";
				}
				else if (object[i].data_type == "Deleted registry") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Deleted registry: ";
				}
				else if (object[i].data_type == "Readed registry") {
					str_data = "action_type: " + object[i].action_type + "<br /> full_path: " + object[i].full_path;
					str_type = "Readed registry: ";
				}

				if (i == 0) add_message_block("Result: ", "New data detected.");

				add_message_block(str_type, str_data);
			}

			if (i == 0) add_message_block("Result: ", "New data not detected.");

			// Loading off
			document.getElementById("uploadProperties").style.display = "inline-block";
			document.getElementById("loaderSpinner").style.display = "none";
			document.getElementById("loaderText").style.display = "none";
		}
	}

	form.append("file", file);
	xhttp.open("POST", document.location.href + "upload", true);
	xhttp.send(form);

	// Loading on
	document.getElementById("uploadBlock").innerHTML = "";
	document.getElementById("uploadProperties").style.display = "none";
	document.getElementById("loaderSpinner").style.display = "block";
	document.getElementById("loaderText").style.display = "block";

	// Properties
	document.getElementById("scanTime").value = "";
	document.getElementById("memoryDump").checked = false;
}

function upload_file() {

}

function add_message_block(str_type, str_data) {
	document.getElementById("uploadBlock").innerHTML += "\
		<div id='messageContainer'>\
			<div id='typeContainer'>\
				<p id='messageType'>" + str_type + "</p>\
			</div>\
			<div id='dataContainer'>\
				<p id='messageData'>" + str_data + "</p>\
			</div>\
		</div>";
}