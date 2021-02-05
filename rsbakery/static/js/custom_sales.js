$(document).on('click', '.addMoreBtn', function () {
    var $tr = $(this).closest('.tr_clone');
    var $clone = $tr.clone();
    $clone.find(':text').val('');
    $clone.find('input[type=number]').val('');
    $clone.find('.price').text('-');
    $clone.find('.total').text('-');
    $tr.after($clone);
    $(this).removeClass('addMoreBtn btn-outline-success')
    $(this).addClass('deleteRow btn-outline-danger')
    $(this).text('x')

});

$(document).on('click', '.deleteRow', function () {
    $(this).closest('.tr_clone').remove();
});

$(document).on('change', '.selectItem', function () {
    var id = $(this).val();
    var $klass = $(this).closest('.tr_clone').find('.price')
    console.log('id', id)
    $.get('/sales/get_price/', { 'id': id }, function (res, status) {
        $klass.text(res['price'])
    });
    $(this)
});

$(document).on('change', '.quantity', function () {
    var qty = $(this).val()
    var price = $(this).closest('.tr_clone').find('.price').text()
    var total = qty * price
    $(this).closest('.tr_clone').find('.total').text(total)
    $('table thead th').each(function (i) {
        calculateColumn(i);
    });
});

function calculateColumn(index) {
    var total = 0;
    $('table tr').each(function () {
        var value = parseInt($('.total', this).eq(index).text());
        if (!isNaN(value)) {
            total += value;
        }
    });
    $('.grandTotal').eq(index).text(total);
    $('#total_order_value').val(total);
}