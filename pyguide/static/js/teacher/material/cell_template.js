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
    body += `<div class="w-50">`;
    body += `<textarea id=markdown_section_${id}>`;
    cell_content['source'].forEach(element => {
        body += element;
    });
    body += `</textarea>
            </div>
            <div class="w-50 p-3 bg-white overflow-auto border border-end-0 border-bottom-0 border-top-0 border-5" id="markdown_convert_${id}">
            </div>`;
    return body;
}

export function render_cell(element,index,body)
{
    if(element['cell_type'] == "code")
    {
        body += `<div class="d-flex flex-row mt-3">`;
        body += `<div class="px-2 fs-2 mmn-exec-container me-1"><i class="bi bi-play-circle"id="exec_cell_${index}"></i></div>`;
        body += `<div class="w-100 shadow-lg">`;
        body += `<div class="d-flex flex-row">`;
        body += render_code_cell(element,index);
        body += `</div>`;
        body += `<div class="w-100 my-1" id="tool_bar_${index}">
                    <div class="d-flex flex-row">
                        <div class="w-100 p-2" id="result_cell_${index}">
                        </div>
                        <div class="px-1 fs-4" style="white-space:nowrap;">
                            <i id="insert_md_${index}" class="bi bi-filetype-md" data-bs-toggle="tooltip" data-bs-placement="bottom" title="新增文字區塊"></i>
                            <i id="insert_code_${index}" class="bi bi-filetype-py" data-bs-toggle="tooltip" data-bs-placement="bottom" title="新增程式區塊"></i>
                            <i id="del_${index}" class="bi bi-trash3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="刪除此區塊"></i>
                        </div>
                    </div>
                </div>`;
        body += `</div>`;
        body += `</div>`;
    }
    if(element['cell_type'] == "markdown")
    {
        body += `<div class="d-flex flex-row mt-3">`;
        body += render_markdown_cell(element,index);
        body += `</div>`;
        body += `<div class="w-100 my-1" id="tool_bar_${index}">
                    <i id="insert_md_${index}" class="bi bi-filetype-md fs-2" data-bs-toggle="tooltip" data-bs-placement="bottom" title="新增文字區塊"></i>
                    <i id="insert_code_${index}" class="bi bi-filetype-py fs-2" data-bs-toggle="tooltip" data-bs-placement="bottom" title="新增程式區塊"></i>
                    <i id="del_${index}" class="bi bi-trash3 fs-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="刪除此區塊"></i>
                </div>`;
    }
    return body
}


export function source_split(str)
{
    let return_array = Array();
    str.indexOf("\n",0);
    let n = 0;
    return_array = str.split("\n");
    return_array.forEach((element,index) => {
        return_array[index] = element.concat("\n");
    });
    return return_array;
}