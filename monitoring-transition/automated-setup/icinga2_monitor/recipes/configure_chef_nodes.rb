require 'json'

target_envs = ['stage1', 'stage2']

target_envs.each do |env|
  mon_hosts = search(:node, "chef_environment:#{env}")

  icinga2_hostgroup env do
    display_name env
  end

  mon_hosts.each do |host|
    host['roles'].each do |role|
      icinga2_hostgroup role do
        display_name role
      end
    end

    icinga2_host host['name'] do
      import 'generic-host'
      display_name host['name']
      address host['address']
      check_command 'hostalive'
      groups [env, host['roles']].flatten
      custom_vars :os => host['os'], :roles => host['roles']
    end
  end
end
