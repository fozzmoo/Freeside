<%= header('View Configuration', menubar( 'Main Menu' => $p,
                                     'Edit Configuration' => 'config.cgi' ) ) %>

<% my $conf = new FS::Conf; my @config_items = $conf->config_items; %>

<% foreach my $section ( qw(required billing username password UI session
                            apache BIND shell
                           ),
                         '', 'depreciated') { %>
  <%= table("#cccccc", 2) %>
  <tr>
    <th colspan="2" bgcolor="#dcdcdc">
      <%= ucfirst($section || 'unclassified') %> configuration options
    </th>
  </tr>
  <% foreach my $i (grep $_->section eq $section, @config_items) { %>
    <tr>
      <td><a name="<%= $i->key %>">
        <b><%= $i->key %></b>&nbsp;-&nbsp;<%= $i->description %>
      </a></td>
      <td><table border=0>
        <% foreach my $type ( ref($i->type) ? @{$i->type} : $i->type ) {
             my $n = 0; %>
          <% if ( $type eq '' ) { %>
            <tr><td><font color="#ff0000">no type</font></td></tr>
          <% } elsif ( $type eq 'textarea' ) { %>
            <tr><td bgcolor="#ffffff">
              <pre><%= join("\n", $conf->config($i->key) ) %></pre>
            </td></tr>
          <% } elsif ( $type eq 'checkbox' ) { %>
            <tr><td bgcolor="#<%= $conf->exists($i->key) ? '00ff00">YES' : 'ff0000">NO' %></td></tr>
          <% } elsif ( $type eq 'text' )  { %>
            <tr><td bgcolor="#ffffff"><%=  $conf->exists($i->key) ? $conf->config($i->key) : '' %></td></tr>
          <% } else { %>
            <tr><td>
              <font color="#ff0000">unknown type <%= $type %></font>
            </td></tr>
          <% } %>
        <% $n++; } %>
      </table></td>
    </tr>
  <% } %>
  </table><br><br>
<% } %>

</body></html>
