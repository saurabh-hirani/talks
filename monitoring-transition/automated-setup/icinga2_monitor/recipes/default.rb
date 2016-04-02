include_recipe '%s::base' % cookbook_name
include_recipe '%s::icinga2' % cookbook_name
include_recipe '%s::configure_chef_nodes' % cookbook_name
include_recipe '%s::configure_aws_nodes' % cookbook_name
include_recipe '%s::configure_xyz_nodes' % cookbook_name
include_recipe '%s::configure_checks' % cookbook_name
