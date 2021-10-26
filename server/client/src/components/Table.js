import * as React from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import { visuallyHidden } from '@mui/utils';
import Title from './Title';
import { Avatar } from '@mui/material';
import axios from 'axios';
import Geocode from 'react-geocode';
import Loader from './Loader';

// function createData(name, address, count, photo) {
//   return {
//     name,
//     address,
//     count,
//     photo
//   };
// }

// const rows = [
//   createData('Cupcake', 'Av. Brasil 2371', 3.7, 'images/stop.png'),
//   createData('Donut', 'Lucas Obes 1081', 25.0, 'images/ceda.png'),
//   createData('Eclair', 'Venancio Benavidez 3187', 16.0, 'images/stop.png'),
//   createData('Frozen yoghurt', 'Av. Brasil 1023', 6.0, 'images/stop.png'),
//   createData('Gingerbread', 'Propios y Av. Italia', 16.0, 'images/ceda.png'),
//   createData('Honeycomb', 'Suarez y Bulevar Artigas', 3.2, 'images/stop.png'),
//   createData('Ice cream sandwich', 'Camino Carrasco km 287 esq. Camino mendoza', 9.0, 'images/ceda.png'),
//   createData('Jelly Bean', 'Suarez y Bulevar Artigas', 0.0, 'images/ceda.png'),
//   createData('KitKat', 'Camino Carrasco km 287 esq. Camino mendoza', 26.0, 'images/ceda.png'),
//   createData('Lollipop', 'Av. Brasil 2371', 0.2, 'images/stop.png'),
//   // createData('Marshmallow', 'Propios y Av. Italia', 0, 'images/stop.png'),
// ];

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

// This method is created for cross-browser compatibility, if you don't
// need to support IE11, you can use Array.prototype.sort() directly
function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) {
      return order;
    }
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

const headCells = [
  {
    id: 'photo',
    numeric: false,
    disablePadding: true,
    label: '',
  },
  {
    id: 'name',
    numeric: false,
    disablePadding: false,
    label: 'Nombre',
  },
  {
    id: 'address',
    numeric: false,
    disablePadding: true,
    label: 'Dirección',
  },
  {
    id: 'count',
    numeric: true,
    disablePadding: false,
    label: 'Cantidad',
  },
];

function EnhancedTableHead(props) {
  const { order, orderBy, onRequestSort } = props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? 'right' : 'left'}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
              style={{ fontWeight: 'bold' }}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

EnhancedTableHead.propTypes = {
  onRequestSort: PropTypes.func.isRequired,
  order: PropTypes.oneOf(['asc', 'desc']).isRequired,
  orderBy: PropTypes.string.isRequired,
};

export default function EnhancedTable() {
  const [rows, setRows] = React.useState([]);
  const [order, setOrder] = React.useState('desc');
  const [orderBy, setOrderBy] = React.useState('count');
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const [loading, setLoading] = React.useState(false);

  const getAddressFromCoordinates = async (coord) => {
    try {
      const addr = await Geocode.fromLatLng(coord[0], coord[1]);
      return addr.results[0].formatted_address;
    } catch (error) {
      return `[${coord[0]}, ${coord[1]}]`;
    }
  };

  React.useEffect(() => {
    const fetchSigns = async () => {
      setLoading(true);
      const res = await axios('http://localhost:3000/signs/locations');
      let signs = res.data.data.data;
      for (const sign of signs) {
        sign.address = await getAddressFromCoordinates(sign.location.coordinates);
      }
      setRows(signs);
      setLoading(false);
    };

    // Geocoder
    Geocode.setApiKey(process.env.REACT_APP_GOOGLE_API_KEY);
    Geocode.setLanguage('es');
    Geocode.setRegion('es');
    Geocode.setLocationType('ROOFTOP');

    if (rows.length === 0) fetchSigns();
  }, [rows]);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleClick = (event, name) => {
    // TODO:
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

  return (
    <Box sx={{ width: '100%' }}>
      <Title>Señales</Title>
      {loading ? (
        <Loader />
      ) : (
        <React.Fragment>
          <TableContainer>
            <Table sx={{ minWidth: 750 }} aria-labelledby="tableTitle" size="medium">
              <EnhancedTableHead
                order={order}
                orderBy={orderBy}
                onRequestSort={handleRequestSort}
              />
              <TableBody>
                {/* if you don't need to support IE11, you can replace the `stableSort` call with:
                 rows.slice().sort(getComparator(order, orderBy))*/}
                {stableSort(rows, getComparator(order, orderBy))
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => {
                    const labelId = `enhanced-table-checkbox-${index}`;

                    return (
                      <TableRow
                        hover
                        onClick={(event) => handleClick(event, row.sign.name)}
                        key={row._id}
                      >
                        <TableCell>
                          <Avatar variant="square" alt="Stop" src={`images/${row.sign.sign}.png`} />
                        </TableCell>
                        <TableCell component="th" id={labelId} scope="row">
                          {row.sign.name}
                        </TableCell>
                        <TableCell padding="none">{row.address}</TableCell>
                        <TableCell align="right">{row.count}</TableCell>
                      </TableRow>
                    );
                  })}
                {emptyRows > 0 && (
                  <TableRow
                    style={{
                      height: 53 * emptyRows,
                    }}
                  >
                    <TableCell colSpan={6} />
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={rows.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </React.Fragment>
      )}
    </Box>
  );
}
