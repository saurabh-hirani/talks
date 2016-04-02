icinga2_applyservice 'check_all_disks' do
  display_name 'Check All Disks'
  check_command 'disk'
  custom_vars :warning => 20, :critical => 10
  assign_where ['host.vars.os == "linux"']
end
