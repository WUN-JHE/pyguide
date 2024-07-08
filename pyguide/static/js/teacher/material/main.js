import { render_cell, source_split } from './cell_template.js';

var material_object = "";
var md_editors = [];
var code_editors = [];


var tooltipTriggerList = "";
var tooltipList = "";

var converter = new showdown.Converter()

function save_material()
{
    $.ajax({
        type: "POST",
        url: "/save_material_content/",
        data: {
            "material_id":material,
            'cells':JSON.stringify(material_object)
        },
        dataType: "json",
        success: function (response) {
            alert(response);
            render_html_by_material_content();
        }
    });
}

function load_material_content_form_file()
{
    $.ajax({
        type: "POST",
        url: "/get_material_content/",
        data: {
            "material_id":material,
        },
        dataType: "json",
        success: function (response) {
            console.log(response['cells']);
            material_object = response['cells'];
            render_html_by_material_content();
        }
    });
}

function render_html_by_material_content()
{

    if(tooltipList)
    {
        tooltipList.forEach(element => {
            element.dispose();
        });
    }

    if( code_editors.length != 0 )
    {
        code_editors.forEach(element => {
            element.editor.off();
        });
    }
    if( md_editors.length != 0 ){
        md_editors.forEach(element => {
            element.editor.off();
        });
    }

    let body = "";
    
    material_object.forEach((element,index) => {
        body = render_cell(element,index,body);
    });
    $("#main_section").html(body);
    tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    //做出cm物件
    material_object.forEach((element,index) => {
        if(element['cell_type'] == "code")
        {
            let editor = CodeMirror.fromTextArea(
                document.getElementById(`code_section_${index}`),{
                    mode: {name: "python",
                            version: 3,
                            singleLineStringErrors: false},
                    lineNumbers:true,
                    lineWrapping:true,
                    tabSize:4,
                    smartIndent:false,
                    indentWithTabs:true,
            });
            code_editors.push({'editor':editor,'id':index});
        }
        else if(element['cell_type'] == "markdown")
        {
            let editor = CodeMirror.fromTextArea(
                document.getElementById(`markdown_section_${index}`),{
                    mode: "markdown",
                    lineNumbers:true,
                    allowDropFileTypes: ["image/png", "image/jpeg", "image/gif"],
            });
            md_editors.push({'editor':editor,'id':index});
            let body = "";
            element['source'].forEach(element => {
                body += element;
            });
            $(`#markdown_convert_${index}`).html(converter.makeHtml(body));
            $(`#markdown_convert_${index}`).addClass("markdown-body");
        }
    });
    //設定cm物件listener
    md_editors.forEach((element,index)=> {
        element.editor.on("drop", function (editor, e) {
            var files = e.dataTransfer.files;
            var reader = new FileReader();
            reader.onloadend = function(){
                var cursor = editor.getCursor();
                editor.replaceRange(`![Alt text](${reader.result})`, cursor);
            }
            reader.readAsDataURL(files[0]);
        })
        element.editor.on('change', function(cm, event){
            console.log(cm.getValue());
            $(`#markdown_convert_${element.id}`).html(converter.makeHtml(cm.getValue()));
            material_object[element.id]['source'] = source_split(cm.getValue());
        });
        element.editor.on('blur', function(cm, event){
            $(`.collapse`).collapse('hide');
        });
    });
    code_editors.forEach((element,index)=> {
        element.editor.on('change', function(cm, event){
            console.log(cm.getValue());
            material_object[element.id]['source'] = source_split(cm.getValue());
        });
        element.editor.on('blur', function(cm, event){
            $(`.collapse`).collapse('hide');
        });
    });
    for (let index = 0; index < material_object.length; index++) 
    {
        $(`#del_${index}`).click(function (e) {
            material_object.splice(index, 1);
            render_html_by_material_content();
        });
        $(`#insert_md_${index}`).click(function (e) {
            $(`#insert_md_${index}`).off("click");
            let item = {
                "cell_type": "markdown",
                "source": []
            };
            material_object.splice(index + 1, 0, item);
            render_html_by_material_content();
        });
        $(`#insert_code_${index}`).click(function (e) {
            $(`#insert_code_${index}`).off("click");
            let item = {
                "cell_type": "code",
                "source": []
            };
            material_object.splice(index + 1, 0, item);
            render_html_by_material_content();
        });
        $(`#exec_cell_${index}`).click(function (e) { 
            console.log(material_object[index]);
            let code = "";
            material_object[index]['source'].forEach(element => {
                code += element;
            });
            let socket_data = {
                'code':code,
                'cell_index':index
            }
            socket.send(JSON.stringify(socket_data));
        });
    }
}
$("#save_file").click(function (e) { 
    save_material();
});

$("#disconnect").click(function (e) { 
    socket.close();
});
$("#reconnect").click(function (e) { 
    init_socket();
});

function init_socket()
{
    //socket = new WebSocket('ws://192.168.50.92:5566');
    socket = new WebSocket('ws://140.116.226.223:5566');
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data);
        $(`#result_cell_${data['cell_index']}`).html(data['code']);
    };

    socket.onopen = (e) => {
        console.log('連接');
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () =>{
        console.log("連線斷開");
    }
}


var socket = "";


$(document).ready(function () {

    init_socket();
    load_material_content_form_file();

});