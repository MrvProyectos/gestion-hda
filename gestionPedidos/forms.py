from django import forms
from django.forms import ModelForm
from .models import Pedidos, Articulos, Fmhingreso, Fmhmovimiento, Fmhpago

# datepicker
from bootstrap_datepicker_plus import DatePickerInput

class FormularioContacto(forms.Form):

    asunto=forms.CharField()
    email=forms.EmailField()
    mensaje=forms.CharField()

class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos

        fields = ['nombre', 'seccion', 'precio']

# =========================
# Finantial Managment House
# =========================

# Períodos
CHOICE_PERIODO = [
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
    ('2024', '2024'),
    ('2025', '2025'),
    ('2026', '2026'),
    ('2027', '2027'),
    ('2028', '2028'),
    ('2029', '2029'),
    ('2030', '2030'),
]

# Meses
CHOICE_MESES = [
    ('01', 'Enero'),
    ('02', 'Febrero'),
    ('03', 'Marzo'),
    ('04', 'Abril'),
    ('05', 'Mayo'),
    ('06', 'Junio'),
    ('07', 'Julio'),
    ('08', 'Agosto'),
    ('09', 'Septiembre'),
    ('10', 'Octubre'),
    ('11', 'Noviembre'),
    ('12', 'Diciembre'),
]

# Tipos de Ingreso
CHK_TIPING = [
    ('ING01', 'Remuneraciones'),
    ('ING02', 'Retornos'),
    ('ING03', 'Bonos'),
    ('ING04', 'Otros Ingresos'),
]

# Tipo de Movimientos (gastos)
CHK_TIPMOV = [
    ('GTO01', 'Financieros'),
    ('GTO02', 'Fijos'),
    ('GTO03', 'Autopistas'),
    ('GTO04', 'Tecnología'),
    ('GTO05', 'Gastos Médicos'),
    ('GTO06', 'Colegios'),
    ('GTO07', 'Supermercado'),
    ('GTO08', 'Contribuciones'),
    ('GTO09', 'Otros Gastos'),
]

# Medio de Pago para Form pago de Documentos
CHK_MEDPAG = [
    ('000', '---'),
    ('EFE', 'Efectivo'),
    ('DEB', 'Debito'),
    ('CRD', 'Credito'),
    ('TRF', 'Transferencia Bancaria'),
    ('CHQ', 'Cheque'),
    ('NCR', 'Nota Credito'),
]

# Tipos de Documento para Form pago de Documentos
CHK_TIPDOC = [
    ('000', '---'),
    ('BOL', 'Boleta'),
    ('FAC', 'Factura'),
    ('OTR', 'Otros Dcto.'),
]

# Codigos de Bancos
CHK_BCO = [
    ('000', '----------'),
    ('001', 'Banco De Chile'),
    ('009', 'Banco Internacional'),
    ('012', 'Banco del estado de Chile'),
    ('014', 'Scotiabank Chile'),
    ('016', 'Banco De Credito E Inversiones'),
    ('028', 'Banco Bice'),
    ('031', 'Hsbc Bank-Chile'),
    ('037', 'Banco Santander-Chile'),
    ('039', 'Itaú Corpbanca'),
    ('049', 'Banco Security'),
    ('051', 'Banco Falabella'),
    ('053', 'Banco Ripley'),
    ('055', 'Banco Consorcio'),
    ('504', 'Scotiabank Azul Ex-Bbva'),
]

# Formulario Ingresos
# ===================
class FormIngreso(forms.ModelForm):

    ingcodtipo = forms.ChoiceField(label='Codigo de Ingreso', choices=CHK_TIPING, widget=forms.Select(attrs={'class': 'form-control'}))
    ingGlosa = forms.CharField(label='Concepto', max_length=70, 
                               widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Concepto'}))
    ingValor = forms.IntegerField(label='Valor', widget=forms.TextInput(attrs={'class':'form-control',
                                                                 'placeholder':'Monto Ingreso'}))
    class Meta:
        model = Fmhingreso

        fields = ['ingcodtipo', 'ingGlosa', 'ingValor']

# Formulario para actualizar ingresos del periodo
# ===============================================
class Formacting(forms.ModelForm):

    id = forms.IntegerField(disabled=True)
    ingcodtipo = forms.ChoiceField(label='Codigo de Ingreso', choices=CHK_TIPING, widget=forms.Select(attrs={'class': 'form-control'}))
    ingGlosa = forms.CharField(max_length=70, 
                               widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Concepto'}))
    ingValor = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control',
                                                                 'placeholder':'Monto Ingreso'}))

    class Meta:
        model = Fmhingreso

        fields = ['id', 'ingcodtipo', 'ingGlosa', 'ingValor']

# Formulario Ingreso de Movimientos
# =================================
class FormIngmvtos(forms.ModelForm):
    movcodtipo = forms.ChoiceField(choices=CHK_TIPMOV, widget=forms.Select(attrs={'class': 'form-control'}))
    movglosa = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Concepto'}))
    movmto = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mto. Movimiento'}))

    class Meta:
        model = Fmhmovimiento

        fields = ['movcodtipo', 'movglosa', 'movmto']

# Formulario Actualizacion de Movimientos
# =======================================
class Formmvtos(forms.ModelForm):

    # define widget formulario
    id = forms.IntegerField(disabled=True)
    movcodtipo = forms.ChoiceField(choices=CHK_TIPMOV, widget=forms.Select(attrs={'class': 'form-control'}))
    movglosa = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Concepto'}))
    movmto = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mto. Movimiento'}))

    class Meta:
        model = Fmhmovimiento

        fields = ['id', 'movcodtipo', 'movglosa', 'movmto']

# ================
# Formulario Pagos
# ================
class Formpagos(forms.ModelForm):

    # Widget del Formulario
    id = forms.IntegerField(disabled=True, widget=forms.TextInput(attrs={'size': '15'}))
    pagidrefmov = forms.IntegerField(disabled=True, widget=forms.TextInput(attrs={'size': '15'}))
    pagfecha = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'))

    pagglosamov = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #
    pagMedpag = forms.ChoiceField(required=True, choices=CHK_MEDPAG, widget=forms.Select(attrs={'class': 'form-control'}))
    pagNumchq = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'N° Cheque'}))
    pagCodbco = forms.ChoiceField(choices=CHK_BCO, widget=forms.Select(attrs={'class': 'form-control'}))
    #
    pagtipdcto = forms.ChoiceField(choices=CHK_TIPDOC, widget=forms.Select(attrs={'class': 'form-control'}))
    pagnumdocu = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nro. Documento'}))
    #
    pagmtomov = forms.IntegerField(disabled=True, widget=forms.TextInput(attrs={'size':'15'}))
    pagmtopago = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Monto Pagado'}))
    #
    pagestado = forms.BooleanField()

    class Meta:
        model = Fmhpago
        fields = ['id', 'pagidrefmov', 'pagfecha', 'pagglosamov', 'pagMedpag', 'pagNumchq', 'pagCodbco', 'pagtipdcto', 'pagnumdocu', 'pagmtomov', 'pagmtopago', 'pagestado']

# Formulario Consulta de Saldos
class FormSldPeriodo(forms.Form):

    # Widget del Formulario
    periodo = forms.ChoiceField(required=True, choices=CHOICE_PERIODO, widget=forms.Select(
        attrs={'autofocus': 'autofocus',
               'class': 'form-control'}))
    meses = forms.ChoiceField(required=True, choices=CHOICE_MESES, widget=forms.Select(attrs={'class': 'form-control'}))