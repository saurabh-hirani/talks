icinga2_applyservice 'check_http' do
  display_name 'HTTP'
  check_command 'http'
  custom_vars :http_uri => '/icinga2-classicui'
  assign_where ['"app" in host.vars.roles']
  ignore_where ['host.name == "app-3"']
end

icinga2_applyservice 'check_procs' do
  display_name 'Total processes'
  check_command 'procs'
  assign_where ['"infra" in host.vars.roles']
end

icinga2_applyservice 'check_users' do
  display_name 'Check users'
  check_command 'users'
  custom_vars :warning => 20, :critical => 50
  assign_where ['host.vars.os == "linux"']
end

icinga2_applyservice 'check_disk' do
  display_name 'Check disk'
  check_command 'disk'
  custom_vars :warning => 20, :critical => 10, :disk_partitions => ["/"]
  assign_where ['host.vars.os != "linux"']
end
