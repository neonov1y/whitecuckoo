document.getElementById("memoryDump").checked = false;

function menu(link) {
	switch (link) {
		case 1:
			document.getElementById("art1").style.display = "block";
			document.getElementById("art2").style.display = "none";
			break;
		case 2:
			document.getElementById("art1").style.display = "none";
			document.getElementById("art2").style.display = "block";
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
			document.getElementById("instruction").style.WebKitAnimation = "showInst 0.5s ease-in-out forwards";
			document.getElementById("instruction").style.MozAnimation = "showInst 0.5s ease-in-out forwards";
			break;
		case "hide":
			document.getElementById("instLinkHide").style.display = "none";
			document.getElementById("instLinkShow").style.display = "inline";

			document.getElementById("instText").style.display = "none";
			document.getElementById("instruction").style.animation = "hideInst 0.5s ease-in-out forwards";
			document.getElementById("instruction").style.WebKitAnimation = "hideInst 0.5s ease-in-out forwards";
			document.getElementById("instruction").style.MozAnimation = "hideInst 0.5s ease-in-out forwards";
			window.setTimeout(function() {document.getElementById("instruction").style.display = "none";},500);
			break;
		default:
			break;
	}
}

function request_process(server_function) {
	if (server_function == "file_add") var file = document.getElementById("uploadFile").files[0];
	else var file = {"size": 0}

	var xhttp = new XMLHttpRequest();
	var form = new FormData();

	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			var str_data = "";
			var str_type = "";
			object = JSON.parse(xhttp.responseText);

			for (var i = 0;i < object.length;i++) {
				str_data = object[i].message;
				str_type = object[i].data_type;
				add_message_block(str_type, str_data);
			}
			// Loading off
			loading(0);
		}
	}

	if (file.size/1024/1024 < 40 || server_function == "clear_list" || server_function == "learn_set" || server_function == "statistic_reset") {
		form.append("function_type", server_function);
		if (server_function == "file_add") {
			form.append("memory_dump", document.getElementById("memoryDump").checked);
			form.append("file", file);
		}
		xhttp.open("POST", document.location.origin + "/upload_process", true);
		xhttp.send(form);

		// Loading on
		loading(1);
	}
	else {
		document.getElementById("uploadBlock").innerHTML = "";
		add_message_block("Message", "File to much big, maximal size is 40M. Your file size: " + (file.size/1024/1024).toFixed(2).toString() + "M");
	}
}

function loading(switch_var) {
	switch (switch_var) {
		case 1:
			document.getElementById("uploadBlock").innerHTML = "";
			document.getElementById("uploadProperties").style.display = "none";
			document.getElementById("loaderSpinner").style.display = "block";
			document.getElementById("loaderText").style.display = "block";
			document.getElementById("memoryDump").checked = false;
			break;
		case 0:
			document.getElementById("uploadProperties").style.display = "block";
			document.getElementById("loaderSpinner").style.display = "none";
			document.getElementById("loaderText").style.display = "none";
			break;
	}
}

function add_message_block(str_type, str_data) {
	var str_color = "#FF4500";
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