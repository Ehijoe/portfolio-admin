function addTag() {
    const tag = document.getElementById('new-tag')?.value;
    const tag_list = document.getElementById('tags');
    if (tag && tag_list) {
        const tag_elem = document.createElement("li");
        tag_elem.className = "tag-item";
        tag_elem.innerHTML = `<input style="width: ${tag.length + 2}ch;" readonly name="tags[]" value="${tag}" type="text" class="tag"/>`;
        const close_button = document.createElement("img");
        close_button.src = '/admin-static/close.png';
        close_button.className = 'close-button';
        close_button.onclick = () => {
            tag_elem.remove();
        }
        tag_elem.appendChild(close_button);
        tag_list.appendChild(tag_elem);
    } else {
        console.log('HTML error');
    }
}
