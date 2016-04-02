include_recipe 'icinga2'
include_recipe 'apache2'
include_recipe 'php'

apache_module 'version' do
  enable true
end

directory "#{node['apache']['dir']}/conf.d" do
  action :create
  recursive true
end

# include upstream icinga2 recipes
include_recipe 'icinga2::server'
include_recipe 'icinga2::server_apache'
include_recipe 'icinga2::server_classic_ui'
include_recipe '%s::api' % cookbook_name
