import { render_cell, source_split, change_status } from './cell_template.js';

var material_object = "";
var md_editors = [];
var code_editors = [];

var tooltipTriggerList = "";
var tooltipList = "";

var converter = new showdown.Converter()

function save_log(index, type)
{
    $.ajax({
        type: "POST",
        url: "/series_log_api/save_log",
        data: {
            'student_material':material,
            'cell_index':index,
            'log_type':type,
        },
        dataType: "json",
        success: function (response) {
            console.log(response);
        }
    });
}

function save_material()
{
    $.ajax({
        type: "POST",
        url: "/student_save_material_content/",
        data: {
            "material_id":material,
            'cells':JSON.stringify(material_object)
        },
        dataType: "json",
        success: function (response) {
            alert(response);
            render_html_by_material_content();
            $("#file_status").html('已儲存');
            $("#file_status").removeClass('text-danger');
            $("#file_status").addClass('text-success');
        }
    });
}


function load_material_content_from_file()
{
    $.ajax({
        type: "POST",
        url: "/student_get_material_content/",
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
                    //readOnly:true,
            });
            code_editors.push({'editor':editor,'id':index});
        }
        else if(element['cell_type'] == "markdown")
        {
            let body = "";
            element['source'].forEach(element => {
                body += element;
            });
            $(`#markdown_convert_${index}`).html(converter.makeHtml(body));
            $(`#markdown_convert_${index}`).addClass("markdown-body");
        }
    });
    //設定cm物件listener
    code_editors.forEach((element,index)=> {
        element.editor.on('change', function(cm, event){
            let type = change_status(material_object[element.id]['source'], cm.getValue());
            save_log(element.id, type);//儲存操作序列
            material_object[element.id]['source'] = source_split(cm.getValue());
            $("#file_status").html('未儲存');
            $("#file_status").removeClass('text-success');
            $("#file_status").addClass('text-danger');
        });
    });
    for (let index = 0; index < material_object.length; index++) 
    {
        //$(`#insert_code_top_${index}`).off("click");
        //$(`#insert_code_bottom_${index}`).off("click");
        //$(`#del_${index}`).off("click");
        $(`#exec_cell_${index}`).off("click");
        /*$(`#del_${index}`).click(function (e) {
            material_object.splice(index, 1);
            render_html_by_material_content();
        });
        $(`#insert_code_top_${index}`).click(function (e) {
            let item = {
                "cell_type": "code",
                "source": []
            };
            material_object.splice(index, 0, item);
            render_html_by_material_content();
        });
        $(`#insert_code_bottom_${index}`).click(function (e) {
            let item = {
                "cell_type": "code",
                "source": []
            };
            material_object.splice(index + 1, 0, item);
            render_html_by_material_content();
        });*/
        //全鎖編輯
        console.log(code_editors);
        code_editors.forEach((element)=> {
            if(element.id == index)
            {
                element.editor.setOption("readOnly", true);
                element.editor.refresh();
                console.log(element.editor);
            }
        });
        //全鎖執行
        $(`#exec_cell_${index}`).removeClass('mmn-exec-btn');
        $(`#exec_cell_${index}`).addClass('mmn-exec-btn-lock');
        $(`#exec_cell_${index}`).prop("disabled",true);
        //上鎖紐全關
        $(`#lock_cell_${index}`).prop("disabled",true);
        //解鎖紐事件-全部解鎖紐關-自己的上鎖扭開-序列開始
        $(`#unlock_cell_${index}`).click(function (e) {
            save_log(index, '序列開始');
            code_editors.forEach((element)=> {
                if(element.id == index)
                {
                    element.editor.setOption("readOnly", false);
                    element.editor.refresh();
                }
            });
            $(`#exec_cell_${index}`).addClass('mmn-exec-btn');
            $(`#exec_cell_${index}`).removeClass('mmn-exec-btn-lock');
            $(`#exec_cell_${index}`).prop('disabled', false);
            for (let index = 0; index < material_object.length; index++) 
            {
                $(`#unlock_cell_${index}`).addClass('mmn-lock-btn-lock');
                $(`#unlock_cell_${index}`).removeClass('mmn-unlock-btn');
                $(`#unlock_cell_${index}`).prop("disabled",true);
            }
            $(`#lock_cell_${index}`).prop("disabled",false);
            $(`#lock_cell_${index}`).removeClass('mmn-lock-btn-lock');
            $(`#lock_cell_${index}`).addClass('mmn-lock-btn');
        });
        //上鎖紐事件-全部解鎖紐開-自己的上鎖紐關-序列結束
        $(`#lock_cell_${index}`).click(function (e) {
            save_log(index, '序列結束');
            code_editors.forEach((element)=> {
                if(element.id == index)
                {
                    element.editor.setOption("readOnly", true);
                    element.editor.refresh();
                }
            });
            $(`#lock_cell_${index}`).addClass('mmn-lock-btn-lock');
            $(`#lock_cell_${index}`).removeClass('mmn-lock-btn');
            $(`#lock_cell_${index}`).prop("disabled",true);
            $(`#exec_cell_${index}`).removeClass('mmn-exec-btn');
            $(`#exec_cell_${index}`).addClass('mmn-exec-btn-lock');
            $(`#exec_cell_${index}`).prop("disabled",true);
            for (let index = 0; index < material_object.length; index++) 
            {
                $(`#unlock_cell_${index}`).prop("disabled",false);
                $(`#unlock_cell_${index}`).removeClass('mmn-lock-btn-lock');
                $(`#unlock_cell_${index}`).addClass('mmn-unlock-btn');
            }
        });
        $(`#exec_cell_${index}`).click(function (e) {
            if ((socket.readyState == 3) || (socket.readyState == 0) || (socket == ""))
            {
                alert('尚未連線，請確認你與連線目標的狀態!!');
            }
            else
            {
                console.log(material_object[index]);
                let code = "";
                material_object[index]['source'].forEach(element => {
                    code += element;
                });
                let socket_data = {
                    "student_material_id":material,
                    'code':code,
                    'cell_index':index,
                    'error_msg':'',
                    'error_type':'',
                    'error_time':'',
                    'error_lineno':'',
                }
                $(`#result_cell_${index}`).html(`<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>`);
                socket.send(JSON.stringify(socket_data));
                $(`#exec_cell_${index}`).removeClass('mmn-exec-btn');
                $(`#exec_cell_${index}`).addClass('mmn-exec-btn-lock');
                $(`#exec_cell_${index}`).prop("disabled",true);
            }
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
    if ((socket.readyState == 3) || (socket.readyState == 0) || (socket == ""))
    {
        init_socket();
    }
    else
    {
        socket.close();
        init_socket();
    }
});

function init_socket()
{
    //socket = new WebSocket('ws://192.168.0.102:5566');
    let now_ip = $("#ip_selection").val();
    socket = new WebSocket('ws://'+now_ip);
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        $(`#exec_cell_${data['cell_index']}`).addClass('mmn-exec-btn');
        $(`#exec_cell_${data['cell_index']}`).removeClass('mmn-exec-btn-lock');
        $(`#exec_cell_${data['cell_index']}`).prop('disabled', false);
        $.ajax({
            type: "POST",
            url: "/response_api/get_res",
            data: data,
            dataType: "json",
            success: function (response) {
                console.log(response);
                $(`#result_cell_${data['cell_index']}`).html(response['code']);
                if(response['error_type'])
                {
                    save_log(response['cell_index'], '執行失敗');
                }
                else
                {
                    save_log(response['cell_index'], '執行成功');
                }
            }
        });
    };

    socket.onopen = (e) => {
        console.log('連接');
        console.log(socket.readyState);
        $("#connection_status").html('已連線');
        $("#connection_status").addClass('text-success');
        $("#connection_status").removeClass('text-danger');
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () =>{
        console.log("連線斷開");
        console.log(socket.readyState);
        $("#connection_status").html('連線中斷');
        $("#connection_status").removeClass('text-success');
        $("#connection_status").addClass('text-danger');
    }
}
$.ajax({
    type: "POST",
    url: "/response_api/get_error_des",
    data: "",
    dataType: "json",
    success: function (response) {
        console.log(response);
    }
});

window.addEventListener("beforeunload", function(event) {
    // 在此處處理事件
    event.returnValue = "離開前請確認檔案是否存檔？";
    for (let index = 0; index < material_object.length; index++)
    {
        if(material_object[index]['cell_type'] == "code")
        {
            if($(`#lock_cell_${index}`).attr('disabled') != "disabled")
            {
                save_log(index, '序列結束');
                code_editors.forEach((element)=> {
                    if(element.id == index)
                    {
                        element.editor.setOption("readOnly", true);
                        element.editor.refresh();
                    }
                });
                $(`#lock_cell_${index}`).addClass('mmn-lock-btn-lock');
                $(`#lock_cell_${index}`).removeClass('mmn-lock-btn');
                $(`#lock_cell_${index}`).prop("disabled",true);
                $(`#exec_cell_${index}`).removeClass('mmn-exec-btn');
                $(`#exec_cell_${index}`).addClass('mmn-exec-btn-lock');
                $(`#exec_cell_${index}`).prop("disabled",true);
                for (let index = 0; index < material_object.length; index++) 
                {
                    $(`#unlock_cell_${index}`).prop("disabled",false);
                    $(`#unlock_cell_${index}`).removeClass('mmn-lock-btn-lock');
                    $(`#unlock_cell_${index}`).addClass('mmn-unlock-btn');
                }
            }
        }
    }
    return "離開前請確認檔案是否存檔？";
});

var socket = "";


$(document).ready(function () {
    //init_socket();
    load_material_content_from_file();
});