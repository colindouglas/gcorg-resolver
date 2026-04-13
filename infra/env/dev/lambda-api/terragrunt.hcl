include {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../../aws//lambda-api"

  before_hook "build_lambda" {
    commands = ["plan", "apply"]
    execute  = ["bash", "${get_repo_root()}/infra/build_lambda.sh"]
  }
}

inputs = {
  lambda_zip_path = "${get_repo_root()}/infra/.build/lambda.zip"
}
