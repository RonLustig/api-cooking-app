# Generated by Django 4.2.11 on 2024-10-29 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookapp', '0005_recipe_ingredients_delete_recipeingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='blacklist',
            field=models.ManyToManyField(blank=True, related_name='blacklisted_by', to='cookapp.ingredient'),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='whitelist',
            field=models.ManyToManyField(blank=True, related_name='whitelisted_by', to='cookapp.ingredient'),
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookapp.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookapp.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'ingredient')},
            },
        ),
    ]
