document.getElementById('all_products_check').addEventListener('change', function () {
    const checkboxes = document.querySelectorAll('input[name="item_ids"]');
    for (const checkbox of checkboxes) {
        checkbox.checked = this.checked;
    }
});
document.getElementById('delete-selected-button').addEventListener('click', function () {
    console.log('delete-selected-button clicked')
    if (!confirm('确定要删除选中的产品吗？')) {
        return;
    }
    const checkboxes = document.querySelectorAll('.product-checkbox:checked');
    const item_ids = [];
    checkboxes.forEach(function (checkbox) {
        item_ids.push(checkbox.value);
    });
    console.log(item_ids);
    if (checkboxes.length === 0) {
        alert('请选择要删除的产品');
        return;
    }
    const hidden_input = document.createElement('input');
    hidden_input.type = 'hidden';
    hidden_input.name = 'item_ids';
    hidden_input.value = item_ids.join(',');
    const form = document.getElementById('delete-selected-form')
    form.appendChild(hidden_input);

    form.submit();
});