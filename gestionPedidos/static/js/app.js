$(".btnPospone").click(function() {
    var valorId ="";
    var valorIdRef ="";
    var valorGlosa ="";
    var valorMmov ="";

    $(this).parents("tr").find("#selectId").each(function() {
        valorId += $(this).html() + "\n";
    });

    $(this).parents("tr").find("#selectIdRef").each(function() {
        valorIdRef += $(this).html() + "\n";
    });

    $(this).parents("tr").find("#selectGlosa").each(function() {
        valorGlosa += $(this).html() + "\n";
    });

    $(this).parents("tr").find("#selectMmov").each(function() {
        valorMmov += $(this).html() + "\n";
    });

    document.getElementById('id_idMod').value = valorId;
    document.getElementById('id_idRef').value = valorIdRef;
    document.getElementById('id_Glosa').value = valorGlosa;
    document.getElementById('id_Mtomov').value = valorMmov;
});