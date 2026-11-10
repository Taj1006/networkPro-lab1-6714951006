"""Contract checks for the unchanged teaching scripts; no real sockets or Docker."""

import contextlib
import io
from pathlib import Path
import runpy
import socket
import unittest
from unittest.mock import MagicMock, call, patch


ROOT = Path(__file__).resolve().parents[1]


class EndDatagrams(Exception):
    """Stop the intentionally infinite UDP server after a finite fake workload."""


class EchoScriptsTests(unittest.TestCase):
    def run_script(self, relative_path, endpoint, messages=(), *, stop_udp=False):
        output = io.StringIO()
        # Patch the real module before run_path imports it: no bind/connect occurs.
        with patch("socket.socket", return_value=endpoint), patch(
            "builtins.input", side_effect=list(messages)
        ), contextlib.redirect_stdout(output):
            if stop_udp:
                with self.assertRaises(EndDatagrams):
                    runpy.run_path(str(ROOT / relative_path), run_name="__main__")
            else:
                runpy.run_path(str(ROOT / relative_path), run_name="__main__")
        return output.getvalue()

    @staticmethod
    def endpoint():
        endpoint = MagicMock()
        endpoint.__enter__.return_value = endpoint
        return endpoint

    def test_tcp_client_sends_multiple_utf8_messages_and_displays_echoes(self):
        endpoint = self.endpoint()
        messages = ["hello", "สวัสดี"]
        endpoint.recv.side_effect = [m.encode() for m in messages]
        output = self.run_script(
            "tcp_echo_server/echo_client.py", endpoint, [*messages, "exit"]
        )
        self.assertEqual(endpoint.sendall.call_args_list,
                         [call(m.encode()) for m in messages])
        for message in messages:
            self.assertIn("Received from server: " + message, output)
        endpoint.__exit__.assert_called_once()

    def test_tcp_client_exit_is_case_insensitive_and_not_transmitted(self):
        endpoint = self.endpoint()
        self.run_script("tcp_echo_server/echo_client.py", endpoint, ["EXIT"])
        endpoint.sendall.assert_not_called()
        endpoint.recv.assert_not_called()

    def test_udp_client_sends_multiple_utf8_messages_and_displays_echoes(self):
        endpoint = self.endpoint()
        messages = ["hello", "สวัสดี"]
        endpoint.recvfrom.side_effect = [
            (m.encode(), ("127.0.0.1", 65432)) for m in messages
        ]
        output = self.run_script(
            "udp_server_test/udp_client.py", endpoint, [*messages, "exit"]
        )
        self.assertEqual(endpoint.sendto.call_args_list, [
            call(m.encode(), ("udp_server", 65432)) for m in messages
        ])
        for message in messages:
            self.assertIn("Received from server: " + message, output)
        endpoint.__exit__.assert_called_once()

    def test_udp_client_exit_is_case_insensitive_and_not_transmitted(self):
        endpoint = self.endpoint()
        self.run_script("udp_server_test/udp_client.py", endpoint, ["ExIt"])
        endpoint.sendto.assert_not_called()
        endpoint.recvfrom.assert_not_called()

    def test_tcp_server_echoes_each_chunk_and_stops_after_disconnect(self):
        listener, connection = self.endpoint(), self.endpoint()
        listener.accept.return_value = (connection, ("127.0.0.1", 12345))
        chunks = [b"first", "สวัสดี".encode(), b"third"]
        connection.recv.side_effect = [*chunks, b""]
        self.run_script("tcp_echo_server/echo_server.py", listener)
        self.assertEqual(connection.sendall.call_args_list, [call(c) for c in chunks])
        self.assertEqual(listener.accept.call_count, 1)
        connection.__exit__.assert_called_once()
        listener.__exit__.assert_called_once()

    def test_tcp_server_handles_immediate_disconnect_without_sending(self):
        listener, connection = self.endpoint(), self.endpoint()
        listener.accept.return_value = (connection, ("127.0.0.1", 12345))
        connection.recv.return_value = b""
        self.run_script("tcp_echo_server/echo_server.py", listener)
        connection.sendall.assert_not_called()

    def test_udp_server_replies_to_each_sender_with_original_bytes(self):
        endpoint = self.endpoint()
        packets = [(b"hello", ("127.0.0.1", 12345)),
                   ("สวัสดี".encode(), ("127.0.0.1", 23456))]
        endpoint.recvfrom.side_effect = [*packets, EndDatagrams()]
        self.run_script("udp_server_test/udp_server.py", endpoint, stop_udp=True)
        self.assertEqual(endpoint.sendto.call_args_list,
                         [call(data, sender) for data, sender in packets])
        endpoint.__exit__.assert_called_once()

    def test_udp_server_echoes_empty_datagram_instead_of_treating_it_as_disconnect(self):
        endpoint = self.endpoint()
        sender = ("127.0.0.1", 12345)
        endpoint.recvfrom.side_effect = [(b"", sender), EndDatagrams()]
        self.run_script("udp_server_test/udp_server.py", endpoint, stop_udp=True)
        endpoint.sendto.assert_called_once_with(b"", sender)


if __name__ == "__main__":
    unittest.main()
