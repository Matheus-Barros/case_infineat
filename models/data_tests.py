import great_expectations as gx
import pandas as pandas

def generate(project_path):

    # project_path = r"C:\Users\MatheusBarros\OneDrive - SDG Group\Documentos\Github\case_infineat\ge"

    context = gx.get_context(mode="file", project_root_dir=project_path)

    data_source = context.data_sources.add_pandas("data_source")
    data_asset = data_source.add_dataframe_asset("data_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("data_batch")

    suite = context.suites.add(
        gx.ExpectationSuite(
            "suite",
            expectations=[
                gx.expectations.ExpectColumnMinToBeBetween(column="valor_total_geral_(r$)", min_value=1, max_value=1000000),
                gx.expectations.ExpectColumnMinToBeBetween(column="pesagem_real_total_(kg)", min_value=1, max_value=1000000),
                
                gx.expectations.ExpectColumnValuesToNotBeNull(column='uf_-_loja'),
                gx.expectations.ExpectColumnValuesToNotBeNull(column='fornecedor'),
                gx.expectations.ExpectColumnValuesToNotBeNull(column='pesagem_real_total_(kg)'),
                gx.expectations.ExpectColumnValuesToNotBeNull(column='valor_total_geral_(r$)'),
                
                gx.expectations.ExpectColumnToExist(column="valor_total_geral_(r$)"),
                gx.expectations.ExpectColumnToExist(column="pesagem_real_total_(kg)")
            ],
        )
    )

    validation_definition = context.validation_definitions.add(gx.ValidationDefinition(name="vd", data=batch_definition, suite=suite))

    context.checkpoints.add(
        gx.Checkpoint(
            name="checkpoint",
            validation_definitions=[validation_definition],
            actions=[gx.checkpoint.actions.UpdateDataDocsAction(name="action")],
        )
    )

def run_tests(project_path,df):
    # project_path = r"C:\Users\MatheusBarros\OneDrive - SDG Group\Documentos\Github\case_infineat\ge"

    context = gx.get_context(mode="file", project_root_dir=project_path)
    batch_parameters = {"dataframe": df}
    cp = context.checkpoints.get('checkpoint')
    cp.run(batch_parameters=batch_parameters)






