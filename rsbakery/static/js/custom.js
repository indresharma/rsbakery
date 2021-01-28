
$(function () {
    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_image").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#modalCrop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("form").submit();
    });

});


$(document).on('click', '.deleteBtn', function () {
    var pk = $(this).attr('data-id');
    var product_delete = $(this).attr('product_delete');
    var stock_delete = $(this).attr('stock_delete');
    var form = $(this).closest('form')[0];
    var url;
    if (product_delete) {
        url = `/dashboard/products/delete/${pk}/`
    } else if (stock_delete){
        url = `/dashboard/stock/delete/${pk}/`
    }
    

    $.ajax({
        type: 'POST',
        url: url,
        data: new FormData(form),
        contentType: false,
        processData: false,
        success: function (res) {
            console.log('Success', res)
            location.reload();
        },
        error: function (res) {
            console.log('Error', res)
        }
    });
});

$(document).on('click', '.addItemBtn', function(){
    let url = "/dashboard/raw_material/add/"
    $.get(url, function (res, status) {
        $('#itemModal').html(res['html'])
        $('#itemModal').modal('show')
    })
});

$(document).on('click', '#saveItem', function(){
    var form = $(this).closest('form')[0]
    var product_stock = $(this).attr('product_stock');
    var url;

    if (product_stock){
        url = '/dashboard/products/stock/add/'
    } else {
        url = `/dashboard/raw_material/add/`
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: new FormData(form),
        contentType: false,
        processData: false,
        success: function (res) {
            console.log('Success', res)
            location.reload();
        },
        error: function () {
            console.log('Error', res)
        }
    });
});

$(document).on('change', '#id_item', function(){
    var pk = $(this).val()
    $.get('/get_unit/', {'pk': pk}, function(res, status){
        $('#unitReadOnly').val(res['unit'])
    });
});


$(document).on('click', '.addProductStockBtn', function(){
    $.get('/dashboard/products/stock/add/', function(res, status) {
        $('#productStockModal').html(res['html']);
        $('#productStockModal').modal('show')
    });
});