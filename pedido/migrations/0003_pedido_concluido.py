from django.db import migrations, models


def marcar_pedidos_antigos_como_concluidos(apps, schema_editor):
    # Os pedidos que já existiam foram feitos antes do botão "Concluir pedido".
    Pedido = apps.get_model('pedido', 'Pedido')
    Pedido.objects.update(concluido=True)


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_alter_pedido_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='concluido',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(marcar_pedidos_antigos_como_concluidos, migrations.RunPython.noop),
    ]
