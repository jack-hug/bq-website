
    document.getElementById('all_products_check').addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('input[name="item_ids"]');
        for (const checkbox of checkboxes) {
            checkbox.checked = this.checked;
        }
    });

    document.getElementById('delete-selected-button').addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('.product-checkbox:checked');
        if (checkboxes.length === 0) {
            alert('请选择要删除的产品');
            return;
        }
        if (!confirm('确定要删除选中的产品吗？')) {
            return;
        }

        const form = document.getElementById('delete-selected-form');
        if (!form) {
            alert('找不到删除表单');
            return;
        }

        // 移除之前可能存在的隐藏输入
        const existingHiddenInputs = form.querySelectorAll('input[name="item_ids"]');
        existingHiddenInputs.forEach(input => form.removeChild(input));

        // 为每个选中的复选框创建一个隐藏输入
        checkboxes.forEach(function (checkbox) {
            const hidden_input = document.createElement('input');
            hidden_input.type = 'hidden';
            hidden_input.name = 'item_ids';
            hidden_input.value = checkbox.value;
            form.appendChild(hidden_input);
        });

        try {
            form.submit();
        } catch (error) {
            alert('提交失败');
            console.error(error);
        }
    });