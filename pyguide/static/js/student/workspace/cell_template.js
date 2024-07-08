function render_code_cell(cell_content, id)
{
    let body = "";
    body += 
    `<div class="w-100"><textarea id=code_section_${id} class="w-100">`;
    cell_content['source'].forEach(element => {
        body += element;
    });
    body += `</textarea></div>`;
    return body;
}

function render_markdown_cell(cell_content,id)
{
    let body = "";
    body += `<div class="w-100 p-3 bg-white overflow-auto mmn-markdown-border" id="markdown_convert_${id}">
            </div>`;
    return body;
}

export function render_cell(element,index,body)
{
    if(element['cell_type'] == "code")
    {
        body += `<div class="d-flex flex-row mb-3">`;
        body += `<div class="px-2 fs-2 mmn-exec-container me-1">
                    <button class="mmn-exec-btn" id="exec_cell_${index}">
                        <i class="bx bx-play"></i>
                    </button>
                    <button class="mmn-unlock-btn" id="unlock_cell_${index}">
                        <i class='bx bxs-lock-open'></i>
                    </button>
                    <button class="mmn-lock-btn-lock" style="margin-bottom:0.5rem;" id="lock_cell_${index}">
                        <i class='bx bxs-lock '></i>
                    </button>
                </div>`;
        body += `<div class="w-100 shadow-lg">`;
        body += `<div class="d-flex flex-row">`;
        body += render_code_cell(element,index);
        body += `</div>`;
        body += `<div class="w-100 my-1" id="tool_bar_${index}">
                    <div class="d-flex flex-column">
                        <div class="w-100 px-2 mb-2" id="result_cell_${index}">
                        </div>
                    </div>
                </div>`;
        body += `</div>`;
        body += `</div>`;
        /*
        <div class="px-1 fs-4" style="white-space:nowrap;">
                            <i class="bi bi-arrow-bar-up"></i>
                            <i id="insert_code_top_${index}" class="bi bi-filetype-py" data-bs-toggle="tooltip" data-bs-placement="bottom" title="往上新增程式區塊"></i>
                            <i class="bi bi-three-dots-vertical"></i>
                            <i class="bi bi-arrow-bar-down"></i>
                            <i id="insert_code_bottom_${index}" class="bi bi-filetype-py" data-bs-toggle="tooltip" data-bs-placement="bottom" title="往下新增程式區塊"></i>
                            <i class="bi bi-three-dots-vertical"></i>
                            <i id="del_${index}" class="bi bi-trash3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="刪除此區塊"></i>
                        </div>
        */
    }
    if(element['cell_type'] == "markdown")
    {
        body += `<div class="d-flex flex-row mb-2">`;
        body += render_markdown_cell(element,index);
        body += `</div>`;
    }
    return body
}


export function source_split(str)
{
    let return_array = Array();
    str.indexOf("\n",0);
    let n = 0;
    //console.log(str);
    return_array = str.split("\n");
    //console.log(return_array);
    return_array.forEach((element,index) => {
        if( index != (return_array.length-1) )
        {
            return_array[index] = element.concat("\n");
        }
    });
    return return_array;
}

export function change_status(src,cm)
{
    let src_len = 0;
    src.forEach(element => {
        src_len += element.length;
    });
    let diff = cm.length - src_len;
    if( diff == 1 )
    {
        return "新增";
    }
    else if( diff > 1 )
    {
        return "貼上";
    }
    else if( diff == -1)
    {
        return "刪除";
    }
    else if( diff < -1 )
    {
        return "剪下";
    }
    else
    {
        return "剪下";
    }
}