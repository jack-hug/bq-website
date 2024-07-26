// // 添加产品名称重复时提示
// $(document).ready(function() {
//     $('#name').on('blur', function() {
//         var name = $(this).val();
//         if (name) {
//             $.ajax({
//                 url: '{{ url_for("admin.check_product_name") }}',
//                 method: 'GET',
//                 data: { name: name },
//                 success: function(response) {
//                     if (response.exists) {
//                         $('#name-error').text('产品名称已存在，请选择其他名称。');
//                     } else {
//                         $('#name-error').text('');
//                     }
//                 },
//                 error: function() {
//                     $('#name-error').text('检查名称时出错，请稍后再试。');
//                 }
//             });
//         } else {
//             $('#name-error').text('');
//         }
//     });
// });
//
// // 假设使用 jQuery 发送 AJAX 请求
// $.ajax({
//     url: '/product/new',
//     type: 'POST',
//     data: form_data,
//     success: function(response) {
//         // 在这里，response 包含了产品 ID
//         var productId = response.product_id;
//
//         // 使用产品 ID 上传图片
//         $.ajax({
//             url: '/upload',
//             type: 'POST',
//             data: { file: imageFile, product_id: productId },
//             success: function(response) {
//                 console.log('图片上传成功');
//             },
//             error: function(error) {
//                 console.error('图片上传失败:', error);
//             }
//         });
//     },
//     error: function(error) {
//         console.error('产品创建失败:', error);
//     }
// });


