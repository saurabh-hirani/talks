icinga2_endpoint node.name do
  host '0.0.0.0'
  port 5665
end

icinga2_zone 'master' do
  endpoints [node.name]
end

# execute api setup
execute 'icinga2 api setup' do
  command 'icinga2 api setup'
  not_if { ::File.exists? node['icinga2']['conf_d_dir'] + '/api-users.conf' }
  notifies :restart, "service[icinga2]"
end

# link objects.d/api-users.conf to conf.d/users.conf
link node['icinga2']['objects_dir'] + '/api-users.conf' do
  to node['icinga2']['conf_d_dir'] + '/api-users.conf'
  not_if { ::File.exists? node['icinga2']['objects_dir'] + '/api-users.conf' }
  notifies :restart, "service[icinga2]"
end
